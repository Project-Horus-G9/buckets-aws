import json
import boto3

def filtro(dados):
    # horario: 5h as 19h
    # razao temp > 2 ou < 0.5
    # energia gerada > 20
    # energia esperada > 20
    # tensao > 5
    
    dados_filtrados = []
        
    for painel in dados['horus']:

        painel_filtrado = {
            "painel_id": painel['painel_id'],
            "setor": painel['setor'],
            "dados": []
        }        

        for dado in painel['dados']:
            if dado['data_hora'].split()[1] in ['05:00:00', '19:00:00']:
                painel_filtrado['dados'].append(dado)
            elif dado['razao_temp'] > 2 or dado['razao_temp'] < 0.5:
                painel_filtrado['dados'].append(dado)
            elif dado['energia_gerada'] > 20:
                painel_filtrado['dados'].append(dado)
            elif dado['energia_esperada'] > 20:
                painel_filtrado['dados'].append(dado)
            elif dado['tensao'] > 5:
                painel_filtrado['dados'].append(dado)
        
        dados_filtrados.append(painel_filtrado)
    
    print("Filtro aplicado!")
    print(f"Quantidade de dados filtrados: {len(dados_filtrados)}")
    
    return dados_filtrados

def salvar_dados(dados, ambiente):

    if ambiente == "local":
        print("Salvando dados localmente")
        
        with open('data_client.json', 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
            
        print("Dados salvos localmente")
        
    elif ambiente == "s3":
        
        print("Salvando dados no S3")
        
        s3 = boto3.client('s3')
        
        body = json.dumps(dados)
        
        bucket_name = 'horus-client'
        object_key = 'data_client.json'
        
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=body)
        
        print("Dados salvos no S3")
    
def estrutura_dados(dados):
    
    dados_estruturados = {"horus": []}
    
    for painel in dados:
        painel_existe = False
        
        for painel_json in dados_estruturados['horus']:
            if painel_json['painel_id'] == painel['painel_id']:
                painel_existe = True
                break
              
        if not painel_existe:
            dados_estruturados['horus'].append(painel)
            
        else:
            for painel_json in dados_estruturados['horus']:
                if painel_json['painel_id'] == painel['painel_id']:
                    painel_json['dados'] = painel['dados']
                    
    return dados_estruturados

def puxar_dados(ambiente):
    
    if ambiente == 'local':
        
        with open('data_trusted.json', 'r') as arquivo:
            dados_json = json.load(arquivo)
            
        return dados_json
    
    elif ambiente == 's3':
        
        s3 = boto3.client('s3')
        
        bucket_name = 'tote-trusted'
        object_key = 'data_trusted.json'
        
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        
        dados_json = json.loads(response['Body'].read().decode('utf-8'))
        
        return dados_json

def main():
    
    session = boto3.Session()
    
    ambiente = "local"
    # ambiente = "s3"
    
    dados_trusted = puxar_dados(ambiente)
        
    dados_filtrados = filtro(dados_trusted)
    
    dados_estruturados = estrutura_dados(dados_filtrados)
    
    salvar_dados(dados_estruturados, ambiente)
    
if __name__ == "__main__":
    main()
        