import pandas as pd

def transform_data(input_file="raw_data.parquet", output_file="aggregated.csv"):
    df = pd.read_parquet(input_file)
    print(df.columns)
    print(df.head())

    # Exemplo de agregação simples
    index = df.columns[0]  # Supondo que a primeira coluna seja 'log_id'
    summary = df.groupby(index).size().reset_index(name="count")

    summary.to_csv(output_file, index=False)
    print(f"Arquivo {output_file} gerado com {len(summary)} registros.")
