from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import service as service
from flask import Flask, jsonify
import json
import logging

# Configurações de conexão
connect = "" # essa conection string é relacionada aos containers ou seja para pegar é só acessar storage account e ir em acess keys
container = "horus-container"
download = "../azure_codes/dados.json"

app = Flask(__name__)

@app.route('/dados', methods=['GET'])
def get_data():
    try:
        service.coleta_de_dados(connect, container, download)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    file_path = '../azure_codes/dados.json'
    data_list = []

    # Ler o JSON linha por linha
    with open(file_path, "r") as json_file:
        for line in json_file:
            try:
                data = json.loads(line)
                data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                print(f"Posição do erro: {e.pos}")
                print(f"Linha do erro: {e.lineno}, Coluna do erro: {e.colno}")

    return jsonify(data_list)



if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(
        func=service.coleta_de_dados,
        trigger=IntervalTrigger(minutes=5),
        args=[connect, container, blob, download],
        id='job_coleta_de_dados',
        name='Executa coleta_de_dados a cada 5 minutos',
        replace_existing=True
    )

    # Configuração de logging
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    app.run(debug=True,host='0.0.0.0', port=5000)
