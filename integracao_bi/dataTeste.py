from datetime import datetime

# Obter a data e hora local atual
local_datetime = datetime.now()

# Imprimir a data e hora no formato padrão
print("Data e hora local atual:", local_datetime)

# Formatar a data e hora em diferentes formatos
formatted_datetime_1 = local_datetime.strftime("%d/%H/%M")

dia = int(local_datetime.strftime("%d"))
hora = int(local_datetime.strftime("%H")) + 3
minuto = int(local_datetime.strftime("%M")) - 1
segundo = int(local_datetime.strftime("%S"))

if segundo > 50:
    minuto -1

print("Formato 1 (DD/HH/MM):", formatted_datetime_1)
print("dia: ", dia)
print("hora: ", hora)
print("minuto: ", minuto)


