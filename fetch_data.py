import requests
import pandas as pd
from transform_data import transform_data
from load_to_sql import load_to_sql

def fetch_data(project_id, endpoint, output_file="raw_data.parquet"):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSZW5hbiBGcmVpdGFzIiwidHlwZSI6ImFwaV9rZXkiLCJleHAiOjE3NzkzNzg3MDR9.nBkqk4SY-HlOtfFIPXcroCQ1QJA5jFLypmQp0nrdcoc"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, params={"project_id": project_id}, headers=headers)
    print(f"Status da resposta: {response.status_code, response.reason}")
    response.raise_for_status()

    # Salva o conteúdo binário como parquet
    with open("raw_data.parquet", "wb") as f:
        f.write(response.content)
    print("Arquivo raw_data.parquet salvo com sucesso!")

    # Verifica se o parquet tem linhas
    df = pd.read_parquet("raw_data.parquet")
    if df.empty:
        raise ValueError("O parquet está vazio!")
    print(f"O parquet contém {len(df)} linhas.")

if __name__ == "__main__":
    # Exemplo de uso
    import os
    from dotenv import load_dotenv
    # Carrega variáveis do arquivo .env
    load_dotenv()

    project_id = os.getenv("PROJECT_ID")
    endpoint = os.getenv("DATASET_ENDPOINT")
    endpoint = endpoint.replace("{PROJECT_ID}", project_id)
    fetch_data(project_id, endpoint)
    transform_data()
    load_to_sql()
