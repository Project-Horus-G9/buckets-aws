from flask import jsonify, request, current_app as app
import boto3
import json

session = boto3.Session()

@app.route('/')
def home():
    return jsonify({"message": "Seja bem-vindo a API em Flask!"})

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     sample_data = {
#         "name": "Example",
#         "value": 123
#     }
#     return jsonify(sample_data)

# @app.route('/api/data', methods=['POST'])
# def post_data():
#     data = request.json
#     return jsonify({"received_data": data}), 201

@app.route('/raw', methods=['GET'])
def get_raw():

    s3 = boto3.client('s3')
    
    bucket_name = 'set-raw-api'
    object_key = 'data_raw.json'
    
    dados_raw = json.loads(s3.get_object(Bucket=bucket_name, Key=object_key)['Body'].read())

    return jsonify(dados_raw)

@app.route('/trusted', methods=['GET'])
def get_trusted():
    
    s3 = boto3.client('s3')
    
    bucket_name = 'tote-trusted-api'
    object_key = 'data_trusted.json'
    
    dados_trusted = json.loads(s3.get_object(Bucket=bucket_name, Key=object_key)['Body'].read())
    
    return jsonify(dados_trusted)

@app.route('/client', methods=['GET'])
def get_client():
    
    s3 = boto3.client('s3')
    
    bucket_name = 'horus-client-api'
    object_key = 'data_client.json'
    
    dados_client = json.loads(s3.get_object(Bucket=bucket_name, Key=object_key)['Body'].read())
    
    return jsonify(dados_client)