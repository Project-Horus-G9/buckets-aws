import mysql.connector
import random
import time

host = 'localhost'
user = 'root'
password = 'root'
database = 'horus'
port = 3306

connection = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database,
  port=port)

cursor = connection.cursor()

# # Diana 
# def 

# # Giovanna
# def 

# # Marco 
# def 

# # Pedro 
# def 

# # Victor Hugo 
# def 

# Victor Rubinec
def dados_luminosidade():
  leituras = []
  for dia in range(7):
    nublado = random.randint(1, 5)
    if nublado == 1:
      for hora in range(24):
        if hora in range(6, 18):
          leituras.append(random.uniform(100, 200))
        elif hora in range(18, 20) or hora in range(4, 6):
          leituras.append(random.uniform(100, 150))
        else:
          leituras.append(random.uniform(50, 100))  
    else:
      for hora in range(24):
        if hora in range(6, 18):
          leituras.append(random.uniform(300, 400))
        elif hora in range(18, 20) or hora in range(4, 6):
          leituras.append(random.uniform(250, 300))
        else:
          leituras.append(random.uniform(100, 200))
          
  # data atual somente o dia, sem hora, uma semana atrás
  data_inicial = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')) - 604800
  print(data_inicial)
  print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_inicial)))
  
  for leitura in leituras:
    dataMedicao = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_inicial))
    print(dataMedicao)
    data_inicial += 3600
    
    insert = f"INSERT INTO luminosidade (dataMedicao,luminosidade)VALUES('{dataMedicao}','{leitura}')"
    cursor.execute(insert)
    connection.commit()

  cursor.close()
  connection.close()           

if connection.is_connected():
  print("Connected to MySQL server")
  
  # dados_luminosidade()