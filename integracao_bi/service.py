from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json

def coleta_de_dados(connect_str,container_name,blob_name,download_file_path):
    try:
        dataAtual = 
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client("hub-horus/02/2024/06/14/18/45.json")

        # Baixar blob
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        print(f"Blob {blob_name} baixado com sucesso para {download_file_path}")

        # Ler o JSON baixado
        with open(download_file_path, "r") as json_file:
            for line in json_file:
                try:
                    data = json.loads(line)  # Carrega o JSON da linha atual
                    print("Conteúdo do JSON:")
                    print(json.dumps(data, indent=4))  # Formata o JSON para leitura
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}")
                    print(f"Linha com erro: {line}")
                    print(f"Posição do erro: {e.pos}")
                    print(f"Linha do erro: {e.lineno}, Coluna do erro: {e.colno}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
