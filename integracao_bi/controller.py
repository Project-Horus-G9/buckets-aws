from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import service as service
from flask import Flask, jsonify, request
import json
import logging
import os


app = Flask(__name__)

@app.route('/dados', methods=['GET'])
def get_data():
    try:
        service.coleta_de_dados()
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

@app.route('/dados/setor', methods=['GET'])
def get_data_by_setor():
    setor = request.args.get('setor')
    if not setor:
        return jsonify({"error": "Parâmetro 'setor' é obrigatório"}), 400

    file_path = '../azure_codes/dados.json'
    filtered_data_list = []

    if not os.path.exists(file_path):
        return jsonify({"error": "Arquivo de dados não encontrado"}), 404

    try:
        with open(file_path, "r") as json_file:
            for line in json_file:
                try:
                    data = json.loads(line)
                    data_list = data.get("Body", [])
                    filtered_data_list = [d for d in data_list if d.get("setor") == setor]
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}")
                    print(f"Posição do erro: {e.pos}")
                    print(f"Linha do erro: {e.lineno}, Coluna do erro: {e.colno}")
    except Exception as e:
        print(f"Erro ao ler o arquivo de dados: {e}")
        return jsonify({"error": "Falha ao ler arquivo de dados"}), 500

    return jsonify(filtered_data_list)

@app.route('/dados/painel', methods=['GET'])
def get_data_by_painel():
    painel = request.args.get('painel')
    if not painel:
        return jsonify({"error": "Parâmetro 'painel' é obrigatório"}), 400

    file_path = '../azure_codes/dados.json'
    filtered_data_list = []

    if not os.path.exists(file_path):
        return jsonify({"error": "Arquivo de dados não encontrado"}), 404

    try:
        with open(file_path, "r") as json_file:

            for line in json_file:
                try:
                    data = json.loads(line)  # Ler o JSON como um único objeto
                    data_list = data.get("Body", [])
                    filtered_data_list = [d for d in data_list if d.get("painel") == painel]
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}")
                    print(f"Posição do erro: {e.pos}")
                    print(f"Linha do erro: {e.lineno}, Coluna do erro: {e.colno}")

    except Exception as e:
        print(f"Erro ao ler o arquivo de dados: {e}")
        return jsonify({"error": f"Falha ao ler arquivo de dados: {e}"}), 500

    return jsonify(filtered_data_list)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(
        func=service.coleta_de_dados,
        trigger=IntervalTrigger(minutes=66),
        args=[],
        id='job_coleta_de_dados',
        name='Executa coleta_de_dados a cada 5 minutos',
        replace_existing=True
    )

    # Configuração de logging
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    app.run(debug=True,host='0.0.0.0', port=5000)
