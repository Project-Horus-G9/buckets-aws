# sensor de clima

import requests
import mysql.connector
import matplotlib.pyplot as plt  
import json

API_Key = "cf66d379214da8cbc2e6dbe4064aa622"
city = "santos"
link = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=30&appid={API_Key}&lang=pt_br"

con = requests.get(link, verify=False)
req = con.json()

parametros = {
   "clima": [],
   "nuvens": [],
   "data": [],
}


for item in req["list"]:
   parametros["clima"].append(item["main"]["temp"])
   parametros["nuvens"].append(item["weather"])
   parametros["data"].append(item["dt_txt"])

clima = parametros["clima"]
dia = parametros["data"]

plt.plot(dia, clima, marker="o")
plt.title("Clima em Santos")
plt.xlabel("Dias")

plt.show()

#   print("Gerando dados de clima")
  
#   API_Key = "cf66d379214da8cbc2e6dbe4064aa622"
#   city = "são paulo"
#   link = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=30&appid={API_Key}&lang=pt_br"

#   con = requests.get(link, verify=False)
#   req = con.json()

#   for item in req["list"]:
#     dataMedicao = item["dt_txt"]
#     clima = item["weather"][0]["description"]
#     tempo = item["weather"][0]["main"]
    
#     insert = f"INSERT INTO clima (dataMedicao, clima, tempo)VALUES('{dataMedicao}','{clima}','{tempo}')"
#     cursor.execute(insert)
#     connection.commit()
     
#   print("Dados de clima gerados com sucesso")