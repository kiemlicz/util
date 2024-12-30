import argparse
import asyncio
import ipaddress
import logging
import socket
import threading
import time
# import uvloop


'''
ulimit -n 1000000
sysctl -w net.ipv4.ip_local_port_range="1025    60999"
sysctl -w net.netfilter.nf_conntrack_max=700000
sysctl -w net.ipv4.tcp_mem="1510566 2014094 3021132"
sysctl -w net.core.rmem_default=31457280
sysctl -w net.core.rmem_max=33554432
sysctl -w net.core.wmem_default=31457280
sysctl -w net.core.wmem_max=33554432
sysctl -w net.core.somaxconn=65536
sysctl -w net.core.netdev_max_backlog=65536
sysctl -w net.core.optmem_max=25165824
sysctl -w net.ipv4.udp_mem="15318750 20425020 30637500"
sysctl -w net.ipv4.udp_rmem_min=16384
sysctl -w net.ipv4.udp_wmem_min=16384
for i in {205..230}; do ip addr add 192.168.20.$i/24 dev br0; done
'''

# how to check buffer fullness?

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
parser.add_argument(
    '--proto',
    help="tcp | udp",
    required=False,
    default="TCP"
)
args = parser.parse_args()

logging.basicConfig(
    format='[%(threadName)s] [%(asctime)s] [%(levelname)-8s] %(message)s',
    level=logging.getLevelName(args.log.upper()),
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)

sources = args.sources
ports = int(args.connections)
server_host = args.host
server_port = int(args.port)
proto = args.proto.upper()
port_offset = 1025  # skip low ports
TASKS_ACTIVE = 0
CONNECTIONS = 0
SUCCESS = 0
FAIL = 0
TIMEOUT_CNT = 0
TIMEOUT = 60
OVERSLEEPING = 0
TOTAL_RUNNING = 100000


class TCPEchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost, src, port):
        self.port = port
        self.src = src
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
        log.debug('TCP Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        global CONNECTIONS
        CONNECTIONS = CONNECTIONS - 1
        log.debug(f'({self.src}:{self.port}) The server closed the connection: {exc}')
        self.on_con_lost.set_result(True)


class UDPEchoClientProtocol(asyncio.Protocol): # dropped by ifc?
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        global CONNECTIONS
        CONNECTIONS = CONNECTIONS + 1
        self.transport = transport
        try:
            self.transport.sendto(self.message.encode())
        except Exception as e:
            log.exception("Failed to send UDP data")
            raise e

    def datagram_received(self, data, addr):
        global SUCCESS
        SUCCESS = SUCCESS + 1
        log.debug('UDP Data received: {!r}'.format(data.decode()))
        self.transport.close()

    def error_received(self, exc):
        log.exception('Error received:', exc)

    def connection_lost(self, exc):
        global CONNECTIONS
        CONNECTIONS = CONNECTIONS - 1
        log.debug('Connection closed', exc)
        self.on_con_lost.set_result(True)


def is_port_in_use(host: str, port: int, tpe: socket.SocketKind = socket.SOCK_STREAM) -> bool:
    with socket.socket(socket.AF_INET, tpe) as s:
        return s.connect_ex((host, port)) == 0


async def debug(sem):
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


async def create_client(src, port, message, sem, tcp: bool = True):
    global FAIL, TASKS_ACTIVE, TIMEOUT_CNT
    try:
        await sem.acquire()
        TASKS_ACTIVE = TASKS_ACTIVE + 1
        loop = asyncio.get_running_loop()

        if tcp and is_port_in_use(src, port, socket.SOCK_STREAM): # can't use UDP here
            log.info(f"Port {port} is in use, skipping")
            FAIL = FAIL + 1
            return
        on_con_lost = loop.create_future()
        if tcp:
            transport, protocol = await loop.create_connection(
                lambda: TCPEchoClientProtocol(message, on_con_lost, src, port), host=server_host, port=server_port,
                local_addr=(src, port)
            )
        else:
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: UDPEchoClientProtocol(message, on_con_lost),
                local_addr=(src, port),
                remote_addr=(server_host, server_port),
            )

        try:
            async with asyncio.timeout(TIMEOUT):
                await on_con_lost
        except TimeoutError as e:
            # log.exception(f"Timeout waiting for {(server_host, server_port)}")
            TIMEOUT_CNT = TIMEOUT_CNT + 1
            raise e
        finally:
            transport.close()
    except Exception:
        # log.exception(f"Failed to connect from {(src, port)}")
        FAIL = FAIL + 1
    finally:
        TASKS_ACTIVE = TASKS_ACTIVE - 1
        sem.release()


def display():
    try:
        time.sleep(2)
        log.info(f"Threads count: {threading.active_count()}")
        log.info(f"Tasks active: {TASKS_ACTIVE}")
        log.info(f"Connections count: {CONNECTIONS}")
        log.info(f"Success count: {SUCCESS}")
        log.info(f"Failure count: {FAIL} (timeouts: {TIMEOUT_CNT})")
        log.info(f"=====")
    except Exception:
        log.exception("Failed to display success count")


def display_success_count(orig_loop):
    while True:
        try:
            display()
            if orig_loop is not None:
                log.info(f"Loop scheduled(running): {len(orig_loop._scheduled)}, ready: {len(orig_loop._ready)}")
            log.info(f"=====")
        except Exception:
            log.exception("Failed to display success count")


async def main():
    tasks = []
    sem = asyncio.Semaphore(TOTAL_RUNNING)
    loop = asyncio.get_running_loop()
    # loop.set_debug(True)
    threading.Thread(target=display_success_count, args=[loop], daemon=True).start()

    start_source = ipaddress.IPv4Address(sources[0])
    end_source = ipaddress.IPv4Address(sources[1])
    for src in range(int(start_source), int(end_source) + 1):
        srcip = str(ipaddress.IPv4Address(src))
        for i in range(ports):
            p = i + port_offset
            message = f"client: {i}"
            log.debug(f"Connecting from: {(src, p)}")
            tasks.append(create_client(srcip, p, message, sem, proto == "TCP"))
            #     # t = asyncio.create_task(create_client(src, p, message))
            #     # f = await loop.run_in_executor(pool, t) # this is starved
            #     # tasks.append(f) # wrap with asyncio.create_task
            #
            #     # f = await loop.run_in_executor(None, debug) # this is starved
            # tasks.append(debug())

    log.info(f"Tasks ({len(tasks)}) distributed, waiting for completion")
    await asyncio.gather(*tasks)
    log.info("All tasks completed")


asyncio.run(main())  # original single loop

log.info("The End")
display()
