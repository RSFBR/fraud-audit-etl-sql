import requests
import pandas as pd
from transform_data import transform_data
from load_to_sql import load_to_sql

def fetch_data(project_id, endpoint, token, output_file="raw_data.parquet"):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, params={"project_id": project_id}, headers=headers)
    print(f"Status da resposta: {response.status_code, response.reason}")
    response.raise_for_status()

    # Salva o conteúdo binário como parquet
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"Arquivo {output_file} salvo com sucesso!")

    # Verifica se o parquet tem linhas
    df = pd.read_parquet(output_file)
    df.to_csv("raw_data.csv", index=False, encoding="utf-8")  # Salva como CSV para inspeção
    if df.empty:
        raise ValueError("O parquet está vazio!")
    print(f"O parquet contém {len(df)} linhas.")

if __name__ == "__main__":
    # Exemplo de uso
    import os
    from dotenv import load_dotenv
    # Carrega variáveis do arquivo .env
    load_dotenv(".env.template")

    project_id = os.getenv("PROJECT_ID")
    endpoint = os.getenv("DATASET_ENDPOINT")
    token = os.getenv("TOKEN")
    if not all([project_id, endpoint, token]):
        raise ValueError("Faltam variáveis no .env.template: PROJECT_ID, DATASET_ENDPOINT ou TOKEN")

    endpoint = endpoint.replace("{PROJECT_ID}", project_id)
    fetch_data(project_id, endpoint, token)
    transform_data()
    load_to_sql()
