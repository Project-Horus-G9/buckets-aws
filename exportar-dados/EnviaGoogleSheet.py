from __future__ import print_function
import os.path, decimal,datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import mysql.connector
import Create,Update


'''
    |---------------------------------------------------------------------------------------
    | Conexao()
    |---------------------------------------------------------------------------------------
'''

def Conexao(objetivo):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
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

    if objetivo == 'drive':
        
        service = build("drive", "v3", credentials=creds)
        return service
    
    elif objetivo == 'sheets':

        service = build('sheets', 'v4', credentials=creds)
        return service

'''
    |---------------------------------------------------------------------------------------
    | GetDados()
    |---------------------------------------------------------------------------------------
'''
def GetBanco():
 script = 'SELECT * From dados limit 100'
 
 conexao = mysql.connector.connect(
     host    = 'localhost',
     database= 'horus_db',
     user    = 'root',
     password= 'senha'
 )
 if conexao.is_connected():
     cursor = conexao.cursor()
     cursor.execute(script)
     data = cursor.fetchall()
     cursor.close()
     data = [[float(item) if isinstance(item, decimal.Decimal) else item.strftime('%H:%M') if isinstance(item, datetime.datetime) else item for item in row] for row in data]

     return data

def ProcuraDrive():
    service = Conexao('drive')
    results = service.files().list(
        q=f"name='Horus' and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()
    items = results.get('files', [])
    folder_id = items[0]['id']

    results = service.files().list(
        q=f"'{folder_id}' in parents",  # Consulta para listar os arquivos da pasta
        pageSize=1000,  # Número máximo de arquivos por página (até 1000)
        fields="nextPageToken, files(id, name)"
    ).execute()
    items = results.get('files', [])
    return items

'''

    |---------------------------------------------------------------------------------------
    | Chama Funções
    |---------------------------------------------------------------------------------------
'''


if __name__ == '__main__':
    data = GetBanco()
    files = ProcuraDrive()
    #Update.EnviaRelatorio(data,'17SAemMl_r2fHfxcWbrSbjabmncXHjpJWHyUIZZN1dhE')
    for nomes in data[0][1]:
        for item in files:
            if nomes == item['name']:
                Update.EnviaRelatorio(data,item['id'])
            elif item['name'] == None:
                id = Create.create(nomes)
                Update.EnviaRelatorio(data,id)
    
    #dados     = PuxaDado(in_bucket,in_arq)
    #dados     = EnviaRelatorio([[1,2,3,4,5],[6,7,8,9,10]],"1eEKcc_OzM0UIxrJ8m5xwAbPZ0bVisEZtPUsshjrfadE")

    # id da planilha utilizada para testes: 1TefMaToPs_Y2t49CI97r4DhcbwJgp7JCgRCRI7oR_cg