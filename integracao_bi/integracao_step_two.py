import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/dados', methods=['GET'])
def get_data():
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
    app.run(debug=True, port=5000)
