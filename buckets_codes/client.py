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

def salvar_dados(dados):

    s3 = boto3.client('s3')

    try:
        with open('data_client.json', 'r') as arquivo:
            dados_json = json.load(arquivo)
            print("data_client.json carregado!")
    except FileNotFoundError:
        dados_json = {"horus": []}
        print("data_client.json não encontrado, criando novo arquivo!")
    
    for painel in dados:
        painel_existe = False
        
        for painel_json in dados_json["horus"]:
            if painel_json["painel_id"] == painel["painel_id"]:
                painel_existe = True
                break
            
        if not painel_existe:
            dados_json['horus'].append(painel)
            
        else:
            for painel_json in dados_json['horus']:
                if painel_json['painel_id'] == painel['painel_id']:
                    painel_json['dados'] = painel['dados']
                
                    
    with open('data_client.json', 'w') as arquivo:
        json.dump(dados_json, arquivo, indent=4)

    json_string = json.dumps('data_client.json')

    bucket_name = 'horus-client'
    object_key = 'data_client.json'
    
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=json_string)


    print("data_client.json salvo!")

def main():
    
    session = boto3.Session()
    
    with open('data_trusted.json', 'r') as arquivo:
        dados_json = json.load(arquivo)
        
    dados_filtrados = filtro(dados_json)
    
    salvar_dados(dados_filtrados)
    
if __name__ == "__main__":
    main()
        