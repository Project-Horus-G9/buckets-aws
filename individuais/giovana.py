# sensor de clima

import requests
import mysql.connector

API_Key  = "cf66d379214da8cbc2e6dbe4064aa622"
city     = "são paulo"
link     = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Key}&lang=pt_br"

host        = "localhost"
user        = "root"
password    = "root"
database    = "horus"
port        = 3306

try:
 connection = mysql.connector.connect(
    host        = host,
    user        = user,
    password    = password,
    database    = database,
    port        = port
 )
except mysql.connector.Error as e:
 print(f"Erro ao conectar ao banco de dados: {e}")
 
con = requests.get(link)    # conexão
req = con.json()            # recebimento do json

# ID tempo
id = req["weather"][0]["id"]

# descrição
desc = req["weather"][0]["description"]

# vento em KM/H
wind = req["wind"]["speed"]

# tempo de chuva e quantia
if id >= 200 and id<=531:
 rain = req["rain"]

# Umidade em %
umidade = req["main"]["humidity"]

# Temperatura Atual
temp_at = req["main"]["temp"]
temp_at = round(temp_at - 273) # kelvin -> celcius

temp_max = req["main"]["temp_max"]
temp_max = round(temp_max - 273) # kelvin -> celcius

temp_min = req["main"]["temp_min"]
temp_min = round(temp_min - 273) # kelvin -> celcius

# pressão atmosférica
pres = req["main"]["pressure"]

print(f"Bom dia {city}, hoje seguiremos com clima de {desc}\n")
print(f"Com ventos de: {wind} km/h ")
# print(f"Volume de chuva para a próxima 1 hora: {rain} ")
print(f"A umidade está em {umidade}% ")
print(f"Temperatura atual: {temp_at} ºC")
print(f"Pressão é de: {pres} hPa")
print(f"Hoje teremos temperatura máxima de: {temp_max} ºC e temperatura minima de: {temp_min} ºC.\n")
print("Tenha um ótimo dia!")