import argparse
import asyncio
import logging
import socket
import threading
import time

parser = argparse.ArgumentParser(
    description='Simple client to test network capabilities'
)
parser.add_argument(
    '--sources',
    help="Source hosts to connect from",
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
    format='[%(asctime)s] [%(levelname)-8s] %(message)s',
    level=logging.getLevelName(args.log.upper()),
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)

sources = args.sources
ports = int(args.connections)
server_host = args.host
server_port = int(args.port)
port_offset = 1025  # skip low ports
SUCCESS = 0
FAIL = 0


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        log.debug('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        global SUCCESS
        log.debug('Data received: {!r}'.format(data.decode()))
        SUCCESS = SUCCESS + 1

    def connection_lost(self, exc):
        log.debug('The server closed the connection')
        self.on_con_lost.set_result(True)


def is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


async def create_client(src, port, message):
    global FAIL
    loop = asyncio.get_running_loop()
    if is_port_in_use(src, port):
        log.info(f"Port {port} is in use, skipping")
        FAIL = FAIL + 1
        return

    try:
        on_con_lost = loop.create_future()
        transport, protocol = await loop.create_connection(
            lambda: EchoClientProtocol(message, on_con_lost), host=server_host, port=server_port,
            local_addr=(src, port)
        )
    except Exception:
        log.exception(f"Failed to connect to {(src, port)}")
        FAIL = FAIL + 1
        return

    try:
        await on_con_lost
    finally:
        transport.close()


def display_success_count():
    while True:
        time.sleep(5)
        log.info(f"Success count: {SUCCESS}")
        log.info(f"Failure count: {FAIL}")


async def main():
    tasks = []
    for src in sources:
        for i in range(ports):
            p = i + port_offset
            message = f"client: {i}"
            log.debug(f"Connecting from: {(src, p)}")
            tasks.append(create_client(src, p, message))
    log.info("all connection tasks created, waiting for completion")
    await asyncio.gather(*tasks)


threading.Thread(target=display_success_count, daemon=True).start()

asyncio.run(main())
log.info("The End")
log.info(f"Success count: {SUCCESS}")
log.info(f"Failure count: {FAIL}")
