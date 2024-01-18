import socket
import json
import sqlite3
import time

def send_data_to_server_chaegul(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))
        s.sendall(json.dumps(data).encode('utf-8'))
        
        
while True:
    data = 'hello'
    send_data_to_server_chaegul(data)

    time.sleep(3)