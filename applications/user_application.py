import serial as s
import time
import pickle
import socket

device = ''  # Device's name
received_data = ''  # Received data
num_serie = 0  # Device's serial number
pressao = -1  # Gas cylinder pressure
dados = {}  # Dictionary in which the received data will be stored
data = bytes()  # Received data from the server
HOST = "localhost"  # The server's hostname or IP address
PORT = 40000  # The server's port

while True:
    print('\nConectando à porta COM3...')
    try:
        # Try to connect with the serial port
        ser1 = s.serial_for_url('COM3', 9600, timeout=10)

        if ser1.is_open:
            print('Conectada.\n')

            # Assigns the device's name to the variable
            device = ser1.name

            print('\nRecebendo os dados...')

            # Read the serial data
            received_data = ser1.read_until('UniqueID: 39 39 31 34 31 05 2D 17/55555', 42)

            print('\nTratando os dados...')

            # Data processing
            received_data = received_data.decode('utf-8')
            received_data = received_data.split("/")

            # Devices Serial Number Extraction
            num_serie = received_data[0]
            num_serie = num_serie.split(":")
            num_serie = num_serie[1].split("\r")

            # Pressure Extraction
            pressao = float(data_received[1])

            # Create the dictionary base for the pickling
            dados = {

                "ID": num_serie[0],

                "Dispositivo": device,

                "Dados:": pressao

            }

            # Pickling
            print('Serializando...)
            try:
                file = pickle.dumps(dados)
                print('Serialização completa.')
                """
                Tentar enviar como json, só que tem que converter o json depois para bytes
                """
                  
            except:
                  print('Não foi possível serializar o dicionário.')

            # Connects with the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(b'True')
                data = s.recv(1024)
                data.decode('utf-8')
                data = bool(data)
                if data:
                    print('Conectado.')
                    s.sendall(file)
                    s.close()
                else:
                    print('Não foi possível estabelecer a conexão com o servidor.')

            # Disconnect with the serial port
            print('\nDesconectando...')
            ser1.close()
            print('Desconectado.\n\n')

            # Waiting time until the next reading
            time.sleep(30)
    except FileNotFoundError:
        print('Não foi possível estabelecer a conexão.')
