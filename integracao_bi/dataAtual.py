from datetime import datetime

# Obter a data e hora local atual
local_datetime = datetime.now()

# Imprimir a data e hora no formato padrão
print("Data e hora local atual:", local_datetime)

# Formatar a data e hora em diferentes formatos
formatted_datetime_1 = local_datetime.strftime("%d/%H/%M")

dia = int(local_datetime.strftime("%d"))
hora = int(local_datetime.strftime("%H"))
minuto = int(local_datetime.strftime("%M"))
segundo = int(local_datetime.strftime("%S"))

if segundo > 50:
    minuto -= 1
    if minuto < 0:
        minuto = 59
        hora -= 1
        if hora < 0:
            hora = 23
            dia -= 1



print("Formato 1 (DD/HH/MM):", formatted_datetime_1)
print("dia: ", dia)
print("hora: ", hora)
print("minuto: ", minuto)
print("segundo: ", segundo)
print("hub-horus/02/2024/06/"+ str(dia) + "/" + str(hora) + "/" + str(minuto) + ".json")
print("hub-horus/02/2024/06/16/00/41.json")


