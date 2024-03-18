# sensor de temperatura

import mysql.connector
import random
from datetime import datetime, timedelta
import socket

def get_local_ip():
    try:
        # Cria um socket UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conecta ao Google DNS
        local_ip = s.getsockname()[0]  # Obtém o endereço IP local
        s.close()
        return local_ip
    except Exception as e:
        print("Erro ao obter o endereço IP local:", e)
        return None

# Exemplo de uso
ip = get_local_ip()

host = 'localhost'
user = 'root'
password = 'root'
database = 'metricas'
port = 3306

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

cursor = connection.cursor()

temperaturas = []
sensor = 'Sensor1'

if connection.is_connected():
    print("Connected to MySQL server")

    current_datetime = datetime.now()

    for dias in range(90):
        for hour in range(24): 
            random_temperature = round(random.uniform(15, 30), 2)
            temperaturas.append(random_temperature)

            tabela = 'leitura_temperatura'
            insert = f"INSERT INTO {tabela} (dataMedicao, sensor, temperatura) VALUES ('{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}', '{sensor}', {random_temperature})"
            cursor.execute(insert)
            connection.commit()

            current_datetime += timedelta(hours=1)  

cursor.close()
connection.close()

print(temperaturas)
