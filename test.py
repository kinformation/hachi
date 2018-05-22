from pypacker import psocket
from pypacker.layer12 import ethernet
import socket

ether = ethernet.Ethernet()
# open sockets using the socket handler
# sock_l2 = psocket.SocketHndl(
#     iface_name='{E5EAB18F-ED6E-4366-9313-063C8BB643D3}', mode=psocket.SocketHndl.MODE_LAYER_2)
sock_l3 = psocket.SocketHndl(
    iface_name='{E5EAB18F-ED6E-4366-9313-063C8BB643D3}', mode=psocket.SocketHndl.MODE_LAYER_3)
# send raw bytes
# sock_l2.send(ether.bin())
sock_l3.send(ether.bin(), "169.254.1.10")
# # receive arbitrary bytes
# bts = sock_l2.recv()
# # receive packets: raw bytes will be internally used to create packets
# pkts = socket_l2.recvp(filter=lambda p: p[IP].src=="127.0.0.1", lowest_layer=Ethernet)
# # send packets and auto-match answers: those will be returned
# pkts = socket_l2.sr(Ethernet() + IP() + TCP(), lowest_layer=ethernet.Ethernet)
# print("answer was: %s" % pkts[0])
# # close sockets
sock_l2.close()
sock_l3.close()

socket.IPV6_CHECKSUM
