from __future__ import print_function
from googleapiclient.errors import HttpError
import EnviaGoogleSheet

def create(empresa):
    service = EnviaGoogleSheet.Conexao('sheets')
    try:
     spreadsheet = {{"properties": {"title": empresa}},{"sheets":{"properties":{"title":"DashBoards"}}}}
     spreadsheet = (
        service.spreadsheets()
        .create(body=spreadsheet, fields="spreadsheetId")
        .execute()
    )
     print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
     return spreadsheet.get("spreadsheetId")
    except HttpError as error:
     print(f"An error occurred: {error}")
     return error
    