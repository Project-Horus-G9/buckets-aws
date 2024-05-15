import json
import time
import random
import matplotlib.pyplot as plt
from memory_profiler import memory_usage
import boto3

def gerar_dados(qtd_dias, paineis):

    tempo_inicio_gerar = time.time()
    
    print("Gerando dados")
    
    dados_coletados = []
    
    possiveis_ceus = ["ceu limpo", "algumas nuvens", "chuva leve", "nublado", "nuvens dispersas"]
    
    for painel in paineis:
    
        # data inicial - qtd_dias atrás
        data_inicial = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')) - 86400 * qtd_dias
    
        painel = {
            "painel_id": painel,
            "setor": "setor sul",
            "dados": []
        }
    
        for dia in range(qtd_dias):
            
            ceu_dia = random.choice(possiveis_ceus)
            
            for meia_hora in range(48):
                
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
                
                dado["ceu"] = ceu_dia
                
                dado["data_hora"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_inicial))            
                
                mes = int(time.strftime('%m', time.localtime(data_inicial)))
                hora = int(time.strftime('%H', time.localtime(data_inicial)))
                
                data_inicial += 1800           
                
                # temperatura externa
                if mes in [12, 1, 2]:
                    if hora in range(8, 16):
                        dado["temp_ext"] = round(random.uniform(30, 35), 2)
                    else:
                        dado["temp_ext"] = round(random.uniform(25, 30), 2)
                elif mes in [3, 4, 5]:
                    if hora in range(8, 16):
                        dado["temp_ext"] = round(random.uniform(25, 30), 2)
                    else:
                        dado["temp_ext"] = round(random.uniform(20, 25), 2)
                elif mes in [6, 7, 8]:
                    if hora in range(8, 16):
                        dado["temp_ext"] = round(random.uniform(20, 25), 2)
                    else:
                        dado["temp_ext"] = round(random.uniform(15, 20), 2)
                else:
                    if hora in range(8, 16):
                        dado["temp_ext"] = round(random.uniform(25, 30), 2)
                    else:
                        dado["temp_ext"] = round(random.uniform(20, 25), 2)
                        
                # temperatura interna
                if hora in range(8, 16):
                    dado["temp_int"] = round(random.uniform(dado["temp_ext"], dado["temp_ext"] + 23), 2)
                else:
                    dado["temp_int"] = round(random.uniform(dado["temp_ext"], dado["temp_ext"] + 19), 2)
                    
                # tensão
                if hora in range(8, 16):
                    dado["tensao"] = round(random.uniform(39, 40), 2)
                elif hora in range(16, 19) or hora in range(6, 8):
                    dado["tensao"] = round(random.uniform(24, 30), 2)
                else:
                    dado["tensao"] = round(random.uniform(0, 5), 2)
                
                # uv
                if hora in range(8, 16):
                    ruido = 0.5
                    uv_indice = 5
                else:
                    ruido = 0.1
                    uv_indice = 0.5
                    
                uv_indice += random.uniform(-ruido, ruido)
                uv_indice = max(0, uv_indice)
                
                dado["uv"] = round(uv_indice, 2)                 
                
                # luminosidade
                if dado["ceu"] == "nublado" or dado["ceu"] == "algumas nuvens":
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
                potencia_maxima_NOCT = 100
                percentual_captacao = 0.6
                
                dado["potencia"] = round(random.uniform(40, potencia_maxima_NOCT * percentual_captacao), 2)
                
                if hora < 8 or hora > 16:
                    dado["potencia"] = round(dado["potencia"] * 0.1, 2)
                
                painel["dados"].append(dado)
                
        dados_coletados.append(painel)

        tempo_fim_gerar = time.time()

        tempo_total_gerar = tempo_fim_gerar - tempo_inicio_gerar
        
    print("Dados gerados")
    
    return dados_coletados, tempo_total_gerar

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

    tempo_inicio_salvar = time.time()
    
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
        
    tempo_fim_salvar = time.time()

    tempo_total_salvar = tempo_fim_salvar - tempo_inicio_salvar

    return tempo_total_salvar
    
def main():

    session = boto3.Session()
    
    ambiente = "local"
    # ambiente = "s3"
    
    paineis = []

    for painel in range(10000):
        paineis.append("painel " + str(painel))
    
    dados, tempo_total_gerar = gerar_dados(7, paineis)

    memoria_usada_gerar = memory_usage((gerar_dados, (7, paineis)))
        
    dados_estruturados = estrurar_dados(dados)

    tempo_total_salvar = salvar_dados(dados_estruturados, ambiente)

    memoria_usada_salvar = memory_usage((salvar_dados, (dados_estruturados, ambiente)))
    
    print("Dados gerados com sucesso")

    print("Tempo total para gerar dados: ", tempo_total_gerar)
    print("Tempo total para salvar dados: ", tempo_total_salvar)
    print("Memória usada para gerar dados: ", memoria_usada_gerar)
    print("Memória usada para salvar dados: ", memoria_usada_salvar)

    bar_width = 0.2

    plt.figure(figsize=(6, 4))
    plt.bar(["Gerar dados", "Salvar dados"], [memoria_usada_gerar[0], memoria_usada_salvar[0]], width=bar_width)
    
    plt.xlabel("Operação")
    plt.ylabel("Memória (MB)")
    plt.title("Uso de memória para gerar e salvar dados")
    plt.show()

    plt.figure(figsize=(6, 4))
    plt.bar(["Gerar dados", "Salvar dados"], [tempo_total_gerar, tempo_total_salvar], width=bar_width)
    plt.xlabel("Operação")
    plt.ylabel("Tempo (s)")
    plt.title("Tempo para gerar e salvar dados")
    plt.show()
    
    return True

if __name__ == "__main__":
    main()