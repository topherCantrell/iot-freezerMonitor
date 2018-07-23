import socket

SERVER_IP   = '192.168.1.12'
SERVER_PORT = 7654

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((SERVER_IP,SERVER_PORT))

while True:    
    data, addr = sock.recvfrom(1024)
    print("Message:"+data.decode("utf-8"))
