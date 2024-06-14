from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json

# Configurações de conexão
connect_str = "" # essa conection string é relacionada aos containers ou seja para pegar é só acessar storage account e ir em acess keys
container_name = "horus-container"
blob_name = "hub-horus/02/2024/06/14/18/45.json"
download_file_path = "../azure_codes/dados.json"

try:
    # Criar cliente de serviço blob
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Criar cliente de container
    container_client = blob_service_client.get_container_client(container_name)

    # Criar cliente de blob
    blob_client = container_client.get_blob_client(blob_name)

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
