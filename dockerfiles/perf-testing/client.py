import argparse
import asyncio
import ipaddress
import logging
import socket
import threading
import time

# ulimit -n 1000000
# sysctl -w net.ipv4.ip_local_port_range="1025    60999"
# sysctl -w net.netfilter.nf_conntrack_max=700000
# sysctl -w net.ipv4.tcp_mem="1510566 2014094 3021132"
# for i in {205..230}; do ip addr add 192.168.20.$i/24 dev br0; done

parser = argparse.ArgumentParser(
    description='Simple client to test network capabilities'
)
parser.add_argument(
    '--sources',
    help="Source hosts to connect from (provide start and stop address)",
    required=True,
    nargs='+'
)
parser.add_argument(
    '--host',
    help="host to connect to",
    required=True
)
parser.add_argument(
    '--port',
    help="port to connect to",
    required=False,
    default=8080
)
parser.add_argument(
    '--connections',
    help="number of connections to generate (estimate)",
    required=False,
    type=int,
    default=50000
)
parser.add_argument(
    '--log',
    help="log level (TRACE, DEBUG, INFO, WARN, ERROR)",
    required=False,
    default="INFO"
)
args = parser.parse_args()

logging.basicConfig(
    format='[%(thread)d] [%(asctime)s] [%(levelname)-8s] %(message)s',
    level=logging.getLevelName(args.log.upper()),
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)

sources = args.sources
ports = int(args.connections)
server_host = args.host
server_port = int(args.port)
port_offset = 1025  # skip low ports
TASKS_ACTIVE = 0
CONNECTIONS = 0
SUCCESS = 0
FAIL = 0
OVERSLEEPING = 0
sem = asyncio.Semaphore(100000)
THREAD_COUNT = 2


# pool = concurrent.futures.ThreadPoolExecutor()  # not the safest


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        global CONNECTIONS
        CONNECTIONS = CONNECTIONS + 1
        transport.write(self.message.encode())
        log.debug('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        global SUCCESS
        SUCCESS = SUCCESS + 1
        log.debug('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        global CONNECTIONS
        CONNECTIONS = CONNECTIONS - 1
        log.debug('The server closed the connection')
        self.on_con_lost.set_result(True)


def is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def debug():  # todo loop per thread
    # loop = asyncio.new_event_loop()
    # try:
    try:
        await sem.acquire()

        global FAIL, TASKS_ACTIVE, OVERSLEEPING
        TASKS_ACTIVE = TASKS_ACTIVE + 1
        s = time.perf_counter()
        await asyncio.sleep(5)
        elapsed = time.perf_counter() - s
        if elapsed > 5:
            OVERSLEEPING = OVERSLEEPING + 1
        # log.info(f"DON: {src}:{port}")
        TASKS_ACTIVE = TASKS_ACTIVE - 1

    except Exception:
        log.exception("Failed to acquire semaphore")
    finally:
        sem.release()
    # finally:
    #     loop.close()


async def create_client(src, port, message):
    await sem.acquire()
    # fixme properly handle exeptions and finally (most likely i didnt release semaphore) - test semaphore separately first on small task
    # check returns
    # try:
    #     global FAIL, TASKS_ACTIVE
    #     TASKS_ACTIVE = TASKS_ACTIVE + 1

    # finally:
    #     sem.release()

    # loop = asyncio.get_running_loop()
    # if is_port_in_use(src, port):
    #     log.info(f"Port {port} is in use, skipping")
    #     FAIL = FAIL + 1
    #     return
    #
    # try:
    #     on_con_lost = loop.create_future()
    #     transport, protocol = await loop.create_connection(
    #         lambda: EchoClientProtocol(message, on_con_lost), host=server_host, port=server_port,
    #         local_addr=(src, port)
    #     )
    # except Exception:
    #     log.exception(f"Failed to connect to {(src, port)}")
    #     FAIL = FAIL + 1
    #     return
    #
    # try:
    #     async with asyncio.timeout(60):
    #         await on_con_lost
    # except Exception:
    #     log.exception(f"Timeout waiting for {(src, port)}")
    #     FAIL = FAIL + 1
    # finally:
    #     transport.close()
    #     TASKS_ACTIVE = TASKS_ACTIVE - 1 #
    #     log.info("Connection closed")


def display_success_count(orig_loop):
    while True:
        try:
            time.sleep(2)
            log.info(f"Threads count: {threading.active_count()}")
            log.info(f"Tasks active: {TASKS_ACTIVE}")
            log.info(f"Connections count: {CONNECTIONS}")
            log.info(f"Success count: {SUCCESS}")
            log.info(f"Failure count: {FAIL}")
            log.info(f"Oversleeping count: {OVERSLEEPING}")
            log.info(f"Loop scheduled:{len(orig_loop._scheduled)}, ready: {len(orig_loop._ready)}")
            log.info(f"=====")
        except Exception:
            log.exception("Failed to display success count")


async def schedule(src_ip):
    src = str(ipaddress.IPv4Address(src_ip))
    tasks = []
    for i in range(ports):
        p = i + port_offset
        message = f"client: {i}"
        log.debug(f"Connecting from: {(src, p)}")
        # tasks.append(create_client(src, p, message))
        # t = asyncio.create_task(create_client(src, p, message))
        # f = await loop.run_in_executor(pool, t) # this is starved
        # tasks.append(f) # wrap with asyncio.create_task

        # f = await loop.run_in_executor(None, debug) # this is starved
        tasks.append(debug())

        # with concurrent.futures.ThreadPoolExecutor() as pool:
        # t = asyncio.create_task(create_client(src, p, message))
        # f = await loop.run_in_executor(pool, create_client, src, p, message)
        # tasks.append(f)
    log.info(f"All ({len(tasks)}) connection tasks created, waiting for completion")
    await asyncio.gather(*tasks)
    log.info("All connection tasks completed")

async def distribute(loop_id):
    tasks = []
    start_source = ipaddress.IPv4Address(sources[0])
    end_source = ipaddress.IPv4Address(sources[1])
    for src in range(int(start_source), int(end_source) + 1):
        if src % THREAD_COUNT == loop_id:
            tasks.append(schedule(src))

async def main():
    tasks = []
    loop = asyncio.get_running_loop()
    # loop.set_debug(True)
    threading.Thread(target=display_success_count, args=[loop], daemon=True).start()

    # loops = [
    #     asyncio.new_event_loop(),
    #     asyncio.new_event_loop()
    # ]
    # for l in loops:
    #     threading.Thread(target=lambda: run_loop(l), args=[]).start()

    start_source = ipaddress.IPv4Address(sources[0])
    end_source = ipaddress.IPv4Address(sources[1])
    for src in range(int(start_source), int(end_source) + 1):
        # l = loops[src % len(loops)]
        # l.call_soon_threadsafe(lambda: schedule(src))  # remove

        src = str(ipaddress.IPv4Address(src))
        for i in range(ports):
            p = i + port_offset
            message = f"client: {i}"
            log.debug(f"Connecting from: {(src, p)}")
            # tasks.append(create_client(src, p, message))
        #     # t = asyncio.create_task(create_client(src, p, message))
        #     # f = await loop.run_in_executor(pool, t) # this is starved
        #     # tasks.append(f) # wrap with asyncio.create_task
        #
        #     # f = await loop.run_in_executor(None, debug) # this is starved
            tasks.append(debug())

            # with concurrent.futures.ThreadPoolExecutor() as pool:
            # t = asyncio.create_task(create_client(src, p, message))
            # f = await loop.run_in_executor(pool, create_client, src, p, message)
            # tasks.append(f)
    log.info(f"Tasks ({len(tasks)}) distributed, waiting for completion")
    await asyncio.gather(*tasks)
    log.info("All tasks completed")

asyncio.run(main()) # original single loop
# threads = [threading.Thread(name=f"t{i}", target=asyncio.run, args=(distribute(i),)) for i in range(THREAD_COUNT)]
# for t in threads:
#     t.start()
# for t in threads:
#     t.join()

log.info("The End")
log.info(f"Success count: {SUCCESS}")
log.info(f"Failure count: {FAIL}")
