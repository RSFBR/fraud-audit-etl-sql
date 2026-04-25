import pandas as pd
import os

def transform_data(input_file="raw_data.parquet", output_file="interim/aggregated.csv"):
    df = pd.read_parquet(input_file)
    print(df.head())
    print(df.columns)

    # # Exemplo de agregação simples
    # index = df["transaction_id"] # Assume que a primeira coluna é a categoria para agregação
    # summary = df.groupby(index).size().reset_index(name="count")

    # summary.to_csv(output_file, index=False)
    # print(f"Arquivo {output_file} gerado com {len(summary)} registros.")

    # Critério 1: valor alto em canal externo (já existente)
    high_value_external = (df["amount"] > 10000) & (df["transaction_type"] == "external")

    # Critério 2: mesma conta origem/destino
    same_account = df["account_origin"] == df["account_destination"]

    # Critério 3: moeda estrangeira com valor alto
    foreign_high = (df["currency"] != "BRL") & (df["amount"] > 5000)

    # Critério 4: IP repetido em muitos clientes
    ip_counts = df["device_ip"].map(df["device_ip"].value_counts())
    suspicious_ip = ip_counts > 50

    # Combina critérios
    df["fraud_flag"] = (
        high_value_external | same_account | foreign_high | suspicious_ip
    ).astype(int)

    grouped = (
        df.groupby("account_origin")
          .agg({"fraud_flag": "sum", "amount": "sum"})
          .rename(columns={"fraud_flag": "suspect_count", "amount": "total_amount"})
          .reset_index()
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    grouped.to_csv(output_file, index=False)
    print(f"Arquivo {output_file} gerado com sucesso!")
