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
        "energia_gerada": round(dado['potencia'] * 0.8, 2),
        "energia_esperada": round(dado['uv'] * 10 * 0.8, 2)
      }

      dados_trusted['dados'].append(sub_dados)
    
    dados_refinados.append(dados_trusted)
  
  print("Refinamento pronto")

  return dados_refinados       
        
def salvar_dados(dados):
    
    try:
        with open('data_trusted.json', 'r') as arquivo:
            dados_json = json.load(arquivo)
            print("data_trusted.json carregado!")
    except FileNotFoundError:
        dados_json = {"horus": []}
        print("data_trusted.json não encontrado, criando novo arquivo!")
    
    for painel in dados:
        painel_existe = False
        
        for painel_json in dados_json['horus']:
            if painel_json['painel_id'] == painel['painel_id']:
                painel_existe = True
                break
              
        if not painel_existe:
            dados_json['horus'].append(painel)
            
        else:
            for painel_json in dados_json['horus']:
                if painel_json['painel_id'] == painel['painel_id']:
                    painel_json['dados'] = painel['dados']
                    
    with open('data_trusted.json', 'w') as arquivo:
        json.dump(dados_json, arquivo, indent=4)

    print("data_trusted.json salvo!")

def salvar_s3():
      
  print("Salvando dados no S3")
      
  s3 = boto3.client('s3')
  
  body = open('data_trusted.json', 'rb')
  
  bucket_name = 'tote-trusted'
  object_key = 'data_trusted.json'
  
  s3.put_object(Bucket=bucket_name, Key=object_key, Body=body)

  print("data_trusted.json salvo!")

def main():
  
  session = boto3.Session()
  
  with open('data_raw.json', 'r') as file:
    dados_raw = json.load(file)
  
  dados_refinados = refinamento(dados_raw) 
  
  salvar_s3()

  salvar_dados(dados_refinados)

if __name__ == "__main__":
  main()