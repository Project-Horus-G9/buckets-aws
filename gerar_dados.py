import mysql.connector
import random
import time
import numpy as np

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

# Diana 
def dados_potencia():
  print("Gerando dados de potência")
  
  potencia_maxima_NOCT = 400
  percentual_captacao = 0.4 
  
  data_inicial = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')) - 604800
  
  #teto em 40% da potência máxima em 
  for dia in range(7):
    for hora in range(24):
      potencia_captada = np.random.uniform(0, potencia_maxima_NOCT * percentual_captacao)
      dataMedicao = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_inicial))
      data_inicial += 3600
      insert = f"INSERT INTO potencia (dataMedicao,potencia)VALUES('{dataMedicao}','{potencia_captada}')"
      cursor.execute(insert)
      connection.commit()
      
  print("Dados de potência gerados com sucesso")

# # Giovanna
# def 

# # Marco 
def dados_voltagem():
  print("Gerando dados de voltagem")
  
  leituras = []
  for i in range(0,7):
    for i in range(0,24):
      random_number = random.uniform(38, 40)
      leituras.append(random_number)
      
  data_inicial = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')) - 604800
  datas = []
  voltagens = []
  
  for voltagem in leituras:
      
    dataMedicao = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_inicial))
    data_inicial += 3600

    voltagens.append(voltagem)
    datas.append(time.strftime('%Hh', time.localtime(data_inicial))),
    
    painel = 'A'
    insert = f"INSERT INTO voltagem (dataMedicao,painel,voltagem)VALUES('{dataMedicao}','{painel}',{voltagem})"
    cursor.execute(insert)
    connection.commit()
    
  print("Dados de voltagem gerados com sucesso")

# # Pedro 
# def 

# # Victor Hugo 
# def 

# Victor Rubinec
def dados_luminosidade():
  print("Gerando dados de luminosidade")
  
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
  
  for leitura in leituras:
    dataMedicao = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_inicial))
    data_inicial += 3600
    
    insert = f"INSERT INTO luminosidade (dataMedicao,luminosidade)VALUES('{dataMedicao}','{leitura}')"
    cursor.execute(insert)
    connection.commit()      
    
  print("Dados de luminosidade gerados com sucesso")

if connection.is_connected():
  print("Connected to MySQL server")
  
  # dados_luminosidade()
  # dados_potencia()
  # dados_voltagem()