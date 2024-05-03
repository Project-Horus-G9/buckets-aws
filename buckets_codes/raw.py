import json
import time
import random
import boto3

def gerar_dados(qtd_dias):
    
    print("Gerando dados")
    
    dado = {
        "data_hora": "",
        "temp_ext": 0,
        "temp_int": 0,
        "tensao": 0,
        "uv": 0,
        "luminosidade": 0,
        "potencia": 0,
        "ceu": ""
    }
    
    dados_coletados = []
    
    possiveis_ceus = ["ceu limpo", "algumas nuvens", "chuva leve", "nublado", "nuvens dispersas"]
    
    # data inicial - qtd_dias atrás
    data_inicial = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')) - 86400 * qtd_dias
    
    for dia in range(qtd_dias):
        
        ceu_dia = random.choice(possiveis_ceus)
        
        for meia_hora in range(48):
            
            dado["ceu"] = ceu_dia
            
            dado["data_hora"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_inicial))            
            
            mes = int(time.strftime('%m', time.localtime(data_inicial)))
            hora = int(time.strftime('%H', time.localtime(data_inicial)))
            
            data_inicial += 1800           
            
            # temperatura externa
            if mes in [12, 1, 2]:
                if hora in range(10, 16):
                    dado["temp_ext"] = round(random.uniform(30, 35), 2)
                else:
                    dado["temp_ext"] = round(random.uniform(25, 30), 2)
            elif mes in [3, 4, 5]:
                if hora in range(10, 16):
                    dado["temp_ext"] = round(random.uniform(25, 30), 2)
                else:
                    dado["temp_ext"] = round(random.uniform(20, 25), 2)
            elif mes in [6, 7, 8]:
                if hora in range(10, 16):
                    dado["temp_ext"] = round(random.uniform(20, 25), 2)
                else:
                    dado["temp_ext"] = round(random.uniform(15, 20), 2)
            else:
                if hora in range(10, 16):
                    dado["temp_ext"] = round(random.uniform(25, 30), 2)
                else:
                    dado["temp_ext"] = round(random.uniform(20, 25), 2)
                    
            # temperatura interna
            if hora in range(10, 16):
                dado["temp_int"] = round(random.uniform(dado["temp_ext"], dado["temp_ext"] + 23), 2)
            else:
                dado["temp_int"] = round(random.uniform(dado["temp_ext"], dado["temp_ext"] + 19), 2)
                
            # tensão
            if hora in range(10, 16):
                dado["tensao"] = round(random.uniform(39, 40), 2)
            elif hora in range(16, 19) or hora in range(6, 10):
                dado["tensao"] = round(random.uniform(24, 30), 2)
            else:
                dado["tensao"] = round(random.uniform(0, 5), 2)
            
            # uv
            dado["uv"] = round(random.uniform(0, 15), 2)
            
            if dado["ceu"] == "nubladp" or dado["ceu"] == "algumas nuvens":
                if hora in range(6, 18):
                    dado["luminosidade"] = round(random.uniform(100, 200), 2)
                elif hora in range(18, 20) or hora in range(4, 6):
                    dado["luminosidade"] = round(random.uniform(100, 150), 2)
                else:
                    dado["luminosidade"] = round(random.uniform(50, 100), 2)
            else:
                if hora in range(6, 18):
                    dado["luminosidade"] = round(random.uniform(300, 400), 2)
                elif hora in range(18, 20) or hora in range(4, 6):
                    dado["luminosidade"] = round(random.uniform(250, 300), 2)
                else:
                    dado["luminosidade"] = round(random.uniform(100, 200), 2)    
                    
            # potência
            potencia_maxima_NOCT = 400
            percentual_captacao = 0.4
            
            dado["potencia"] = round(random.uniform(0, potencia_maxima_NOCT * percentual_captacao), 2)
            
            if hora < 6 or hora > 18:
                dado["potencia"] = round(dado["potencia"] * 0.1, 2)
            
            dados_coletados.append(dado)
            
            dado = {
                "data_hora": "",
                "temp_ext": 0,
                "temp_int": 0,
                "tensao": 0,
                "uv": 0,
                "luminosidade": 0,
                "potencia": 0,
                "ceu": ""
            }
            
    return dados_coletados

def salvar_painel(dados, painel, setor):    

    dados_json = {
        "painel_id": painel,
        "setor": setor,
        "dados": []
    }
        
    for dado in dados:
        dados_json["dados"].append(dado)
            
    return dados_json

def estrurar_dados(paineis):
    
    dados_estruturados = {"horus": []}
    
    for painel in paineis:
        dados_estruturados["horus"].append(painel)
                    
    return dados_estruturados
    
def salvar_dados(dados, ambiente):
    
    if ambiente == "local":
        print("Salvando dados localmente")
        
        with open('data_raw.json', 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
            
        print("Dados salvos localmente")
        
    elif ambiente == "s3":
        
        print("Salvando dados no S3")
            
        s3 = boto3.client('s3')
        
        body = json.dumps(dados)
        
        bucket_name = 'set-raw'
        object_key = 'data_raw.json'
        
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=body)
        
        print("Dados salvos no S3")
    
def main():
    
    session = boto3.Session()
    
    ambiente = "local"
    # ambiente = "s3"
    
    dados = gerar_dados(7)
    
    painel1 = salvar_painel(dados, 1, "sul")
    painel2 = salvar_painel(dados, 2, "sul")
    painel3 = salvar_painel(dados, 3, "norte")
    
    paineis = [painel1, painel2, painel3]
    
    dados_estruturados = estrurar_dados(paineis)
    
    salvar_dados(dados_estruturados, ambiente)
    
    print("Dados gerados com sucesso")
    
    return True

if __name__ == "__main__":
    main()