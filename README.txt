# Fraud Audit ETL

Pipeline de auditoria de transações suspeitas.

## Execução em sequência

1. **Carregar variáveis de ambiente**
   - Copie `.env.template` para `.env` e configure os valores necessários (token, endpoint, etc.).

2. **Buscar dados da API**
   ```bash
   python fetch_data.py

    Faz chamada GET na API de datasets.

    Salva raw_data.parquet e raw_data.csv.

3. **Transformar dados**
   ```bash
    python transform_data.py

    Lê raw_data.parquet com pandas.read_parquet.

    Aplica critérios de fraude.

    Gera interim/aggregated.csv.

4. **Carregar no banco**

   ```bash
    python load_to_sql.py

    Cria tabela auditing_summary em auditing.db.
    
    Insere registros do aggregated.csv.

    Valida que pelo menos uma linha foi inserida.

    falha caso não haja registros, como parte da validação final.