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