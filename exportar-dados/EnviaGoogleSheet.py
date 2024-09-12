
'''
    |--------------------------------------------------------------------------------------
    |
    | - Objetivo    : Pegar dados armazenados no bucket S3 e imprimir no Google Sheet
    | - É Requisito?: Sim
    |
    |---------------------------------------------------------------------------------------
    | - Criado: 
    | 04.09.2024 - Giovana
    |---------------------------------------------------------------------------------------
    | - Modificações:
    | 
    | 01.01.9999 - usuário X
    |---------------------------------------------------------------------------------------
'''

'''
    |---------------------------------------------------------------------------------------
    | Import
    |---------------------------------------------------------------------------------------
'''
from __future__ import print_function
import os.path, boto3,json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


'''
    |---------------------------------------------------------------------------------------
    | PuxaDado()
    |---------------------------------------------------------------------------------------
'''
def PuxaDado(bucket_name,file_key):
 s3 = boto3.client('s3')
 response = s3.get_object(Bucket=bucket_name, Key=file_key)

 content = response['Body'].read().decode('utf-8')
 data = json.loads(content)
 return data


'''
    |---------------------------------------------------------------------------------------
    | EnviaRelatorio()
    |---------------------------------------------------------------------------------------
'''
def EnviaRelatorio(dados,in_sheet):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    
    # verifica se já existe o arquivo de autenticação para acesso ao google drive
    if os.path.exists('token.json'):
        # caso exista - carrega o token
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # pega os dados do arquivo client_secret e executa a autenticação
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)    

        # gera o arquivo token    
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Ler informações da Planilha do Google Sheets
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=in_sheet,
                                range='Página1!A1:C12').execute()
    values = result.get('values', dados)
    
    # adicionar/editar valores no Google Sheets
    result = sheet.values().update(spreadsheetId=in_sheet,
                                range='Página1!A2', valueInputOption="RAW",
                                   body={"values": values}).execute()

    print('Dados enviados com Sucesso!')

'''
    |---------------------------------------------------------------------------------------
    | Chama Funções
    |---------------------------------------------------------------------------------------
'''
if __name__ == '__main__':
    in_bucket = input("Digite o nome do bucket:\n>> ")
    in_arq    = input("Digite o nome do arquivo a ser acessado ( não é necessário passar a extensão '.json', apenas o nome):\n>> ")
    in_sheet  = input("Digite o link de acesso a planilha:\n>> ")

    dados     = PuxaDado(in_bucket,in_arq)
    dados     = EnviaRelatorio(dados, in_sheet)

    # id da planilha utilizada para testes: 1TefMaToPs_Y2t49CI97r4DhcbwJgp7JCgRCRI7oR_cg