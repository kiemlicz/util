import argparse
import asyncio
import logging

from prometheus_client import start_http_server, Summary, Counter

# split request from connection
TCP_CONNECTION_TOTAL = Counter('perfserver_tcp_connection_total', 'Total number of TCP connections')
TCP_REQUEST_TIME = Summary('perfserver_tcp_request_processing_seconds', 'Time spent processing tcp request')
UDP_REQUEST_TIME = Summary('perfserver_udp_request_processing_seconds', 'Time spent processing udp request')
# increase(perfserver_tcp_request_processing_seconds_count[10s])
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
# parser.add_argument(
#     '--limit',
#     help="handle at most N requests at a time",
#     required=False,
#     default=1000000
# )
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

HOST = args.host
PORT = int(args.port)
DELAY = int(args.delay)
# RATE_LIMIT = asyncio.Semaphore(args.limit)

class TcpEchoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        TCP_CONNECTION_TOTAL.inc()
        peername = transport.get_extra_info('peername')
        log.info('Connection from {}'.format(peername))
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
        self.transport = transport

    @UDP_REQUEST_TIME.time()
    def datagram_received(self, data, addr):
        message = data.decode()
        log.info('UDP received %r from %s' % (message, addr))
        log.debug('UDP send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)


async def main():
    loop = asyncio.get_running_loop()

    tcp_server = await loop.create_server(
        TcpEchoServerProtocol, HOST, PORT
    )
    # udp_transport, protocol = await loop.create_datagram_endpoint(
    #     UdpEchoServerProtocol,
    #     local_addr=(HOST, PORT)
    # )

    async with tcp_server:
        await tcp_server.serve_forever()


if __name__ == '__main__':
    log.info("Starting prometheus server on port 8000")
    start_http_server(8000)
    log.info(f"Starting server on {HOST}:{PORT}")
    asyncio.run(main())
