# Pipeline de Auditoria

## Pré-requisitos
- Python 3.10+
- Instalar dependências: pip install -r requirements.txt
- Configurar variáveis no arquivo `.env.template`:
  - PROJECT_ID
  - DATASET_ENDPOINT (com placeholder {PROJECT_ID})
  - TOKEN

## Execução em sequência
1. Buscar dados da API:
   python fetch_data.py

   Esse script:
   - Faz chamada GET na API de datasets
   - Salva parquet em raw_data.parquet
   - Executa transform_data()
   - Gera aggregated.csv
   - Executa load_to_sql() para carregar no banco

2. Executar etapas isoladas (opcional):
   - Transformação: python transform_data.py
   - Carga: python load_to_sql.py

## Resultado
- Arquivo `aggregated.csv` gerado em `interim/`
- Banco SQLite `auditing.db` com tabela `auditing_summary` populada