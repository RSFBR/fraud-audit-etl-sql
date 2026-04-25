import pandas as pd
import os

def transform_data(input_file="raw_data.parquet", output_file="interim/aggregated.csv"):
    df = pd.read_parquet(input_file)
    print(df.head())
    print(df.columns)

    # Critério 1: valor alto em canal externo (já existente)
    high_value_external = (df["amount"] > 10000) & (df["transaction_type"] == "external")

    # Critério 2: mesma conta origem/destino
    same_account = df["account_origin"] == df["account_destination"]

    # Critério 3: moeda estrangeira com valor alto
    foreign_high = (df["currency"] != "BRL") & (df["amount"] > 5000)

    # Critério 4: IP repetido em muitos clientes
    ip_counts = df["device_ip"].map(df["device_ip"].value_counts())
    suspicious_ip = ip_counts > 50

    # Critério 5: flag já fornecida pelo dataset
    dataset_flag = df["is_fraud_suspect"].astype(bool)

    # Combina todos os critérios
    df["fraud_flag"] = (
        high_value_external | same_account | foreign_high | suspicious_ip | dataset_flag
    ).astype(int)

    print(df["fraud_flag"].value_counts())  # Verifica quantos suspeitos foram identificados

    # Conta transações suspeitas por cliente
    suspect_count = df.groupby("account_origin")["fraud_flag"].sum()

    # Soma apenas valores suspeitos (amount * fraud_flag)
    suspicious_amount = (df["amount"] * df["fraud_flag"]).groupby(df["account_origin"]).sum()

    # Monta DataFrame final
    grouped = pd.DataFrame({
        "account_origin": suspect_count.index,
        "suspect_count": suspect_count.values,
        "total_amount": suspicious_amount.values
    })

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    grouped.to_csv(output_file, index=False)
    print(f"Arquivo {output_file} gerado com sucesso!")