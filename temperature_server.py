import socket

SERVER_PORT = 7654

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("",SERVER_PORT))

while True:    
    data, addr = sock.recvfrom(1024)
    print("Message:"+data.decode("utf-8"))
