import socket
import json

HOST = ''
PORT = 40000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print('Socket criado!')
sock.listen(5)
print('Esperando conexão...')
conn, addr = sock.accept()
print('Nova conexão de', addr, '!')
sock.sendall(True)
conf = sock.recv(1)
if conf:
  # Abrir arquivo
  json_file = sock.recv(95)
  data = json.loads(json_file.decode('utf-8'))
  arquivo = open('dados_recebidos.json', 'w')
  arquivo.write(data)
  arquivo.close()
  sock.close()
