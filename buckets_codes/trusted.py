import json
import boto3  

def refinamento(dados):

  print("Começamdo o refinamento")

  dados_refinados = []

  for painel in dados['horus']:
    dados_trusted = {
      "painel_id": painel['painel_id'],
      "setor": painel['setor'],
      "dados": []
    }
    
    for dado in painel['dados']:

      sub_dados = {
        "data_hora": dado['data_hora'],
        "temp_ext": dado['temp_ext'],
        "temp_int": dado['temp_int'],
        "tensao": dado['tensao'],
        "luminosidade": dado['luminosidade'],
        "ceu": dado['ceu'],
        "razao_temp": round(dado['temp_int'] / dado['temp_ext'], 2),
        "energia_gerada": round(dado['uv'] * 10 * 0.8, 2),
        "energia_esperada": round(dado['potencia'] * 0.8, 2)
      }

      dados_trusted['dados'].append(sub_dados)
    
    dados_refinados.append(dados_trusted)
  
  print("Refinamento pronto")

  return dados_refinados   

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
     
def salvar_dados(dados, ambiente):
    
    if ambiente == 'local':
      
      print("Salvando dados no arquivo local")
                        
      with open('data_trusted.json', 'w') as arquivo:
          json.dump(dados, arquivo, indent=4)

      print("data_trusted.json salvo!")
      
    elif ambiente == 's3':
      print("Salvando dados no S3")
      
      s3 = boto3.client('s3')

      body = json.dumps(dados)

      bucket_name = 'tote-trusted'
      object_key = 'data_trusted.json'

      s3.put_object(Bucket=bucket_name, Key=object_key, Body=body)

      print("data_trusted.json salvo!")

def puxar_dados(ambiente):
  
  if ambiente == 'local':
    
    with open('data_raw.json', 'r') as arquivo:
      dados_json = json.load(arquivo)
      
    return dados_json
  
  elif ambiente == 's3':
    
    s3 = boto3.client('s3')
    
    bucket_name = 'set-raw'
    object_key = 'data_raw.json'
    
    dados_json = json.loads(s3.get_object(Bucket=bucket_name, Key=object_key)['Body'].read())
    
    return dados_json

def main():
  
  session = boto3.Session()
  
  # ambiente = 'local'
  ambiente = 's3'
  
  dados_raw = puxar_dados(ambiente)
  
  dados_refinados = refinamento(dados_raw) 
  
  dados_estruturados = estrutura_dados(dados_refinados)

  salvar_dados(dados_estruturados, ambiente)

if __name__ == "__main__":
  main()