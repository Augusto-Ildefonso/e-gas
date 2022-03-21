import socket
import pickle
import json
import time

HOST = 'localhost'
PORT = 40000

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print('Socket criado!')
    print('Esperando conexão...')
    conn, addr = sock.accept()
    print('Nova conexão de', addr, '!')
    conf = conn.recv(1024)
    conn.sendall(conf)
    conf.decode('utf-8')
    conf = bool(conf)
    print(conf)
    if conf:
        # Abrir arquivo
        data = conn.recv(1024)
        json_file = pickle.loads(data)
        json = json.dumps(json_file, indent=4)
        file = open('data.json', 'w')
        file.write(json)
        file.close()
        sock.close()
    time.sleep(30)
