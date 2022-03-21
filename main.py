import serial as s
import time
import json
import socket

device = ''  # Variável na qual será armazemada o nome do dispositivo
data_received = ''  # Variável na qual será armazanado os dados recebidos
num_serie = 0  # Variável na qual será armazenada o número de série
pressao = -1  # Variável na qual será armazenada a pressão
dados = {}  # Variável a partir da qual será gerado o arquivo JSON
HOST = "localhost"  # The server's hostname or IP address
PORT = 40000

while True:
    print('\nConectando à porta COM3...')

    # Faz a conexão serial
    ser1 = s.serial_for_url('COM3', 9600, timeout=10)

    if ser1.is_open:
        print('Conectada.\n')

        # Atribue o nome do dispositivo à variável
        device = ser1.name

        print('\nRecebendo os dados...')

        # Lê os dados recebidos via serial
        data_received = ser1.read_until('UniqueID: 39 39 31 34 31 05 2D 17/55555', 42)

        print('\nTratando os dados...')

        # Tratamento dos dados
        data_received = data_received.decode('utf-8')
        data_received = data_received.split("/")

        # Extração do número de série do arduino
        num_serie = data_received[0]
        num_serie = num_serie.split(":")
        num_serie = num_serie[1].split("\r")

        # Extração da pressão
        pressao = float(data_received[1])

        # Criação do dicionário base para o JSON
        dados = {

            "ID": num_serie[0],

            "Dispositivo": device,

            "Dados:": pressao

        }

        # Escrita no arquivo JSON
        file = json.dumps(dados, indent=4)
        print('Arquivo criado.')

        # Conectando com o servidor
        print('Conectando com o servidor...')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        conf = sock.recv(1)  # Recebe True se tiver se conectado ao server
        if conf:
          print('Conectado.')
          sock.sendall(True)  # Envia mensagem de que foi conectado para o server
          sock.sendfile(file)  # Envia o arquivo 
          sock.close()  # Fecha a conexão com o server
        else:
          print('Não foi possível estabelecer a conexão.')

        # Desconecta a conexão serial
        print('\nDesconectando...')
        ser1.close()
        print('Desconectado.\n\n')

        # Tempo de espera até a próxima leitura
        time.sleep(2)
    else:
        print('Não foi possível estabelecer a conexão.')
