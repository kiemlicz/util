import argparse
import asyncio
import logging

import asyncudp
from prometheus_client import start_http_server, Summary, Counter

# split request from connection
TCP_CONNECTION_TOTAL = Counter('perfserver_tcp_connection_total', 'Total number of TCP connections')
UDP_CONNECTION_TOTAL = Counter('perfserver_udp_connection_total', 'Total number of UDP unique sources')
TCP_REQUEST_TIME = Summary('perfserver_tcp_request_processing_seconds', 'Time spent processing tcp request')
UDP_REQUEST_TIME = Summary('perfserver_udp_request_processing_seconds', 'Time spent processing udp request')
# sum(increase(perfserver_tcp_request_processing_seconds_count[2s]))
# sum(increase(perfserver_tcp_connection_total[2s]))
##
# sum(increase(perfserver_udp_request_processing_seconds_count[2s]))
# sum(increase(perfserver_udp_connection_total[2s]))
# query options -> min interval

parser = argparse.ArgumentParser(
    description='Simple server to test network capabilities'
)
parser.add_argument(
    '--host',
    help="host to listen on",
    required=False,
    default="0.0.0.0"
)
parser.add_argument(
    '--port',
    help="port to listen on",
    required=False,
    default=8080
)
parser.add_argument(
    '--delay',
    help="simulation processing delay (tcp only)",
    required=False,
    default=0
)
parser.add_argument(
    '--log',
    help="log level (TRACE, DEBUG, INFO, WARN, ERROR)",
    required=False,
    default="INFO"
)
args = parser.parse_args()

logging.basicConfig(
    format='[%(threadName)s] [%(asctime)s] [%(levelname)-8s] %(message)s',
    level=logging.getLevelName(args.log.upper()),
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)

try:
    import uvloop

    uvloop_enabled = True
    log.info("uvloop installed, using it as default event loop")
except ImportError:
    log.error("uvloop not installed, falling back to default event loop")
    uvloop_enabled = False

HOST = args.host
PORT = int(args.port)
DELAY = int(args.delay)

class TcpEchoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        TCP_CONNECTION_TOTAL.inc()
        peername = transport.get_extra_info('peername')
        log.debug('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        asyncio.create_task(self.handle_data(data))

    @TCP_REQUEST_TIME.time()
    async def handle_data(self, data):
        message = data.decode()
        log.info('TCP received: {!r}'.format(message))

        if DELAY > 0:
            await asyncio.sleep(DELAY)

        log.debug('TCP send: {!r}'.format(message))
        self.transport.write(data)

        log.info('Close the client socket')
        self.transport.close()


class UdpEchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        UDP_CONNECTION_TOTAL.inc()
        self.transport = transport

    def datagram_received(self, data, addr):
        asyncio.create_task(self.handle_data(data, addr))  # delegating to simulate processing delay

    @UDP_REQUEST_TIME.time()
    async def handle_data(self, data, addr):
        message = data.decode()
        log.info('UDP received %r from %s' % (message, addr))

        if DELAY > 0:
            await asyncio.sleep(DELAY)

        log.debug('UDP send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)


@UDP_REQUEST_TIME.time()
def serve(sock, data, addr):
    sock.sendto(data, addr)


@UDP_REQUEST_TIME.time()
async def echo_serve(sock, data, addr):
    if DELAY > 0:
        await asyncio.sleep(DELAY)
    sock.sendto(data, addr)


async def echo_server():
    loop = asyncio.get_running_loop()
    sock = await asyncudp.create_socket(local_addr=(HOST, PORT))
    log.info("Simple server started")
    while True:
        data, addr = await sock.recvfrom()
        # serve(sock, data, addr)
        loop.create_task(echo_serve(sock, data, addr))  # probably garbage implementation


async def main():
    loop = asyncio.get_running_loop()

    tcp_server = await loop.create_server(
        TcpEchoServerProtocol, HOST, PORT
    )
    udp_transport, protocol = await loop.create_datagram_endpoint(
        UdpEchoServerProtocol,
        local_addr=(HOST, PORT)
    )

    async with tcp_server:
        await tcp_server.serve_forever()


if __name__ == '__main__':
    log.info("Starting prometheus server on port 8000")
    start_http_server(8000)
    log.info(f"Starting server on {HOST}:{PORT}")
    if uvloop_enabled:
        uvloop.run(main())
    else:
        asyncio.run(main())
