import serial as s
import time
import json
import requests
import os

device = ''  # Device's name
received_data = ''  # Received data
num_serie = 0  # Device's serial number
pressure = -1  # Gas cylinder pressure
dados = {}  # Dictionary in which the received data will be stored
data = bytes()  # Received data from the server
json_file = ''
url = ''


while True:
    # Try to connect with the serial port
    ser1 = s.serial_for_url('COM3', 9600, timeout=10)
    print('Conectando à porta COM3...')
    if ser1.is_open:
        print('Conectada.\n')
        # Assigns the device's name to the variable
        device = ser1.name

        # Read the serial data
        print('\nRecebendo os dados...')
        received_data = ser1.read(41)  # ID uses 33 bits, ' \r\n' uses 3 bits and the pressure uses 5 bits

        # Data processing
        print(f'Dados recebidos: {received_data}')
        print('\nTratando os dados...')
        received_data = received_data.decode('utf-8')
        received_data = received_data.split(' \r\n')

        # Devices Serial Number Extraction
        num_serie = received_data[0]
        num_serie = num_serie.split(': ')
        num_serie = num_serie[1]
        print('Tratamento concluído.')
        print(f'\n\nATENÇÃO! SEGUE O NÚMERO DE SÉRIE DO SEU DISPOSITIVO PARA QUE SEJA ADICIONADO NO DASHBOARD.'
              f'\nDispositivo: {device}\nNúmero de Série: {num_serie}')

        # Pressure Extraction
        pressure = float(received_data[1])

        # Create the dictionary base for the pickling
        dados = {

            "ID": num_serie,

            "Dispositivo": device,

            "Pressao": pressure

        }

        # Try to serialize the JSON
        print('\n\nCriando o arquivo JSON...')
        try:
            json_file = json.dumps(dados, indent=4)   
        except:
            print('Não foi possível criar o arquivo JSON.')

        # Connects with the server
        print('\nConectando com o servidor...')
        try:
            r = requests.post(url, data=json_file)
        except requests.ConnectionError:
            printd('Não foi possível conectar com o servidor.')
        # Waiting time until the next reading
        time.sleep(10)

        # Clear the terminal
        os.system('cls')
    else:
        print('Não foi possível estabelecer a conexão.')
