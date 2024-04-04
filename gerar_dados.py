import mysql.connector
import random
import time
import numpy as np
import requests
import datetime

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
  
  horas_do_dia = np.linspace(0, 24, 100)
  potencia_maxima_NOCT = 400
  percentual_captacao = 0.4

  potencia_captada = np.random.uniform(0, potencia_maxima_NOCT * percentual_captacao, len(horas_do_dia))
  potencia_captada[horas_do_dia < 6] *= 0.1
  potencia_captada[horas_do_dia > 18] *= 0.1
  
  for i in range(len(horas_do_dia)):
    dataMedicao = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    insert = f"INSERT INTO potencia (dataMedicao,potencia)VALUES('{dataMedicao}',{potencia_captada[i]})"
    cursor.execute(insert)
    connection.commit() 
  
  print("Dados de potência gerados com sucesso")

# Giovanna
def dados_clima():
  print("Gerando dados de clima")
  
  API_Key = "cf66d379214da8cbc2e6dbe4064aa622"
  city = "são paulo"
  link = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=30&appid={API_Key}&lang=pt_br"

  con = requests.get(link, verify=False)
  req = con.json()

  for item in req["list"]:
    dataMedicao = item["dt_txt"]
    clima = item["weather"][0]["description"]
    tempo = item["weather"][0]["main"]
    
    insert = f"INSERT INTO clima (dataMedicao, clima, tempo)VALUES('{dataMedicao}','{clima}','{tempo}')"
    cursor.execute(insert)
    connection.commit()
     
  print("Dados de clima gerados com sucesso")

# Marco 
def dados_voltagem():
  print("Gerando dados de voltagem")
  
  leituras = []
  for i in range(0,7):
    for i in range(0,24):
      random_number = random.uniform(39, 40)
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

# Pedro 
def dados_temperatura_ex():
    print("Gerando dados de temperatura")
    
    def obter_estacao(mes):
      if mes in [12, 1, 2]:
          return "Verão"
      elif mes in [3, 4, 5]:
          return "Outono"
      elif mes in [6, 7, 8]:
          return "Inverno"
      else:
          return "Primavera"

    def gerar_temperatura(estacao):
        if estacao == "Verão":
            return random.uniform(30, 35)
        elif estacao == "Outono":
            return random.uniform(25, 30)
        elif estacao == "Inverno":
            return random.uniform(20, 25)
        else:
            return random.uniform(25, 30)

    dias_semana = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    temperaturas_por_dia = {dia: [] for dia in dias_semana.values()}
    data_atual = datetime.datetime.now()
    dias_simulacao = 7
    horario_inicio_pico = 9
    horario_fim_pico = 15

    for dia in range(dias_simulacao):
        dia_semana = dias_semana[data_atual.strftime("%A")]
        
        for hora in range(horario_inicio_pico, horario_fim_pico + 1):
            for meia_hora in range(0, 60, 30):
                data_hora = datetime.datetime(data_atual.year, data_atual.month, data_atual.day, hora, meia_hora)
                estacao_atual = obter_estacao(data_hora.month)
                temperatura = gerar_temperatura(estacao_atual)
                temperaturas_por_dia[dia_semana].append(temperatura)

        data_atual += datetime.timedelta(days=1)
        
    for dia, temperaturas in temperaturas_por_dia.items():
        for idx, temp in enumerate(temperaturas, start=1):
            dataMedicao = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            dataMedicao += f" {hora}:{meia_hora}:00"
            insert = f"INSERT INTO temperaturaExterna (dataMedicao,temperatura)VALUES('{dataMedicao}',{temp})"
            cursor.execute(insert)
            connection.commit()
    
    print("Dados de temperatura gerados com sucesso")

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
  # dados_clima()
  dados_temperatura_ex()