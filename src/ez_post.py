import socket
import json

def _send_string_cr(sock,s):
    sock.send((s+'\n').encode())
    
def post_to_home_gateway(name,data):
    
    data = json.dumps(data)
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('10.0.0.18',80))
    
    _send_string_cr(sock,'POST /data/'+name+' HTTP/1.1')
    _send_string_cr(sock,'Content-Type: application/json')
    _send_string_cr(sock,'Cache-Control: no-cache')
    _send_string_cr(sock,'content-length: '+str(len(data)))
    _send_string_cr(sock,'')
    _send_string_cr(sock,data)
      
    sock.close()
