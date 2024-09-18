from __future__ import print_function
import EnviaGoogleSheet 
import datetime
import pandas as pd

def EnviaRelatorio(dados,in_sheet):
     service = EnviaGoogleSheet.Conexao('sheets') 
     df = pd.DataFrame(dados)   
 # Ler informações da Planilha do Google Sheets
     sheet = service.spreadsheets()
     result = sheet.values().get(spreadsheetId=in_sheet,
                                 range='Dados!A1:C12').execute()
     values = result.get('values', dados)
    
     # adicionar/editar valores no Google Sheets
     result = sheet.values().update(spreadsheetId=in_sheet,
                                 range='Dados!A2', valueInputOption="RAW",
                                    body={"values": dados}).execute()
    
     print('Dados enviados com Sucesso!')