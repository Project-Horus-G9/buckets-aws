# sensor de temperatura

import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def gerar_temperaturas_epoca_do_ano(num_dias):
    temperaturas = []
    data_hora = datetime.now()

    for dia in range(num_dias):
        mes = dia // 30 + 1

        for hora in range(24):
            data_hora += timedelta(hours=1)
            if mes in [12, 1, 2]:
                temperatura = random.uniform(25, 30)
            elif mes in [3, 4, 5]:
                temperatura = random.uniform(20, 25)
            elif mes in [6, 7, 8]:
                temperatura = random.uniform(10, 25)
            else:
                temperatura = random.uniform(20, 25)

            temperaturas.append((data_hora, temperatura))

    return temperaturas

temperaturas_semanais = gerar_temperaturas_epoca_do_ano(7)

dias_da_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

for dia, temperaturas_dia in enumerate(zip(*[iter(temperaturas_semanais)]*24)):
    print(f"Leituras para {dias_da_semana[dia]}:")
    for hora, temperatura in enumerate(temperaturas_dia, start=1):
        data, temp = temperatura
        print(f"  - Data: {data.strftime('%d/%m/%Y %H:%M:%S')} - Temperatura: {temp:.2f}°C")

    print()

# Plotagem dos gráficos
medias_por_dia = []

fig, axs = plt.subplots(7, 1, figsize=(10, 15), sharex=True)
fig.suptitle('Temperaturas por Dia', fontsize=16)

for dia, temperaturas_dia in enumerate(zip(*[iter(temperaturas_semanais)]*24)):
    horas, temperaturas = zip(*temperaturas_dia)
    axs[dia].plot(horas, temperaturas, marker='o')
    axs[dia].set_title(dias_da_semana[dia])
    axs[dia].set_ylabel('Temperatura (°C)')
    axs[dia].tick_params(axis='x', rotation=45)
    medias_por_dia.append(sum(temperaturas) / len(temperaturas))

plt.figure(figsize=(10, 5))
plt.bar(dias_da_semana, medias_por_dia, color='skyblue')
plt.title('Média de Temperatura por Dia')
plt.xlabel('Dia da Semana')
plt.ylabel('Média de Temperatura (°C)')
plt.show()