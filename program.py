import matplotlib.pyplot as plt
import mysql.connector
import numpy as np

host = 'localhost'
user = 'root'
password = 'root'
database = 'horus'

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database)

cursor = connection.cursor()

voltagem = {
    "dataMedicao": [],
    "painel": [],
    "voltagem": []
}

luminosidade = {
    "dataMedicao": [],
    "luminosidade": []
}

potencia = {
    "dataMedicao": [],
    "potencia": []
}

clima = {
    "dataMedicao": [],
    "clima": [],
    "tempo": []
}

temperaturaExterna = {
    "dataMedicao": [],
    "temperatura": []
}

# temperaturaInterna = {}

def puxarDados():
    cursor.execute("SELECT * FROM voltagem where dataMedicao between '2024-03-26 00:00:00' and '2024-03-26 23:59:59'")
    for dado in cursor:
        hora = dado[1].split(" ")[1].split(":")[0]
        voltagem["dataMedicao"].append(f'{hora}h')
        voltagem["painel"].append(dado[2])
        voltagem["voltagem"].append(dado[3])
        
    cursor.execute("SELECT * FROM luminosidade where dataMedicao between '2024-03-26 00:00:00' and '2024-03-26 23:59:59'")
    for dado in cursor:
        hora = dado[1].split(" ")[1].split(":")[0]
        luminosidade["dataMedicao"].append(f'{hora}h')
        luminosidade["luminosidade"].append(dado[2])
        
    cursor.execute("SELECT * FROM potencia where dataMedicao between '2024-03-26 00:00:00' and '2024-03-26 23:59:59'")
    for dado in cursor:
        hora = dado[1].split(" ")[1].split(":")[0]
        potencia["dataMedicao"].append(f'{hora}h')
        potencia["potencia"].append(dado[2])
        
    cursor.execute("SELECT * FROM clima")
    for dado in cursor:
        dia = dado[1].split(" ")[0]
        clima["dataMedicao"].append(dia)
        clima["clima"].append(dado[2])
        
    cursor.execute("SELECT * FROM temperaturaExterna")
    print(cursor)
    for dado in cursor:
        hora = dado[1].split(" ")[1].split(":")[0]
        temperaturaExterna["dataMedicao"].append(f'{hora}h')
        temperaturaExterna["temperatura"].append(dado[2])
    
    cursor.close()
    
def plotarGraficos():
    # plt.plot(voltagem["dataMedicao"], voltagem["voltagem"])
    # plt.xlabel('Hora')
    # plt.ylabel('Voltagem (Volts)')
    # plt.show()

    # plt.plot(luminosidade["dataMedicao"], luminosidade["luminosidade"])
    # plt.xlabel('Hora')
    # plt.ylabel('Luminosidade (Lumens)')
    # plt.show()

    # plt.figure(figsize=(10, 6))
    # plt.plot(potencia["dataMedicao"], potencia["potencia"], color='blue', label='Potência Captada')
    # plt.axhline(y=400, color='red', linestyle='--', label='Potência Máxima NOCT')
    # plt.xlabel('Período analisado (h)')
    # plt.ylabel('Potência (W)')
    # plt.title('Análise da Placa Solar KuMax CS3U')
    # plt.legend()
    # plt.grid(True)
    # plt.ylim(0, 400 + 50)
    # plt.xticks(np.arange(0, 25, 2))
    # plt.show()

    # clima_unicos = list(set(clima["clima"]))
    # contagem_clima = [clima["clima"].count(clima_unico) for clima_unico in clima_unicos]
    # plt.bar(clima_unicos, contagem_clima)
    # plt.xlabel('Clima')
    # plt.ylabel('Quantidade')
    # plt.show()
    
    plt.plot(temperaturaExterna["dataMedicao"], temperaturaExterna["temperatura"])
    plt.xlabel('Hora')
    plt.ylabel('Temperatura (°C)')
    plt.show()
    
def main():
    puxarDados()
    plotarGraficos()
    
if __name__ == "__main__":
    main()