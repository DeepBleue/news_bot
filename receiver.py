import socket
import json
import sqlite3

def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12345))
        s.listen()

        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)  # Receives up to 1024 bytes
            if data:
                return json.loads(data.decode('utf-8'))
            else:
                return None

while True:
    data = receive_data()
    if data is not None:
        # save_data_to_db(data)
        print(data)
    else:
        pass
