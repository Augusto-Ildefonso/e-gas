import socket
import pickle
import json
import time
import os

HOST = 'localhost'
PORT = 40000

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print('Socket criado!')
    print('\nEsperando conexão...')
    conn, addr = sock.accept()
    print('Nova conexão de', addr, '!')
    print('\n\nRecebendo os dados...')
    conf = conn.recv(1024)
    conn.sendall(conf)
    conf.decode('utf-8')
    conf = bool(conf)
    print('Dados recebidos.')
    if conf:
        # Abrir arquivo
        print('\n\nCriando arquivo JSON...')
        try:
            data = conn.recv(1024)
            file = open('data.json', 'w')
            data = data.decode('utf-8')
            file.write(data)
            file.close()
            print('Arquivo criado.')
        except:
            print('Não foi possível criar o arquivo.')
        sock.close()
        print('Conexão encerrada.\n\n')
    time.sleep(10)
    os.system('cls')
