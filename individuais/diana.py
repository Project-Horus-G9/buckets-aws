#  sensor de potência eletrica

import numpy as np
import matplotlib.pyplot as plt

horas_do_dia = np.linspace(0, 24, 100)  # Horas do dia (de 0 a 24 horas
potencia_maxima_NOCT = 400  # Potência máxima da placa solar em NOCT 
percentual_captacao = 0.4 

#teto em 40% da potência máxima em NOCT
potencia_captada = np.random.uniform(0, potencia_maxima_NOCT * percentual_captacao, len(horas_do_dia))

# Plotando o gráfico
plt.figure(figsize=(10, 6))
plt.plot(horas_do_dia, potencia_captada, color='blue', label='Potência Captada')
plt.axhline(y=potencia_maxima_NOCT, color='red', linestyle='--', label='Potência Máxima NOCT')
plt.xlabel('Período analisado (h)')
plt.ylabel('Potência (W)')
plt.title('Análise da Placa Solar KuMax CS3U')
plt.legend()
plt.grid(True)
plt.ylim(0, potencia_maxima_NOCT + 50)
plt.xticks(np.arange(0, 25, 2))
plt.show()