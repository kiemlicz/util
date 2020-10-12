import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = os.environ.get("UDP_PORT", "9999")

server = (server_address, int(server_port))
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))


while True:
    payload, client_address = sock.recvfrom(16)
    msg = "{}{}\n".format(payload.decode("utf-8"), socket.gethostname())
    print("Echoing data back to " + str(client_address))    
    sent = sock.sendto(msg.encode("utf-8"), client_address)
