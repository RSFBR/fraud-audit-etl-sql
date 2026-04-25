# import pandas as pd
# from sqlmodel import SQLModel, create_engine, Session, Field

# class AuditingSummary(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     account_origin: str
#     suspect_count: int
#     total_amount: float

# def load_to_sql(csv_file="interim/aggregated.csv", db_url="sqlite:///auditing.db"):
#     df = pd.read_csv(csv_file)
#     print(df.head())
#     print(df.columns)

#     engine = create_engine(db_url)
#     SQLModel.metadata.create_all(engine)

#     with Session(engine) as session:
#         for _, row in df.iterrows():
#             record = AuditingSummary(
#                 account_origin=row["account_origin"],
#                 suspect_count=row["suspect_count"],
#                 total_amount=row["total_amount"]
#             )
#             session.add(record)
#         session.commit()
#     print("Registros inseridos em auditing_summary.")

import pandas as pd
from sqlmodel import SQLModel, create_engine, Session, Field, select

# Define a tabela de auditoria
class AuditingSummary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_origin: str
    suspect_count: int
    total_amount: float

def load_to_sql(csv_file="interim/aggregated.csv", db_url="sqlite:///auditing.db"):
    # Lê o CSV gerado pela transformação
    df = pd.read_csv(csv_file)
    print("Pré-visualização dos dados:")
    print(df.head())
    print("Colunas:", df.columns.tolist())

    # Cria engine e tabela
    engine = create_engine(db_url)
    SQLModel.metadata.create_all(engine)

    # Insere registros
    with Session(engine) as session:
        for _, row in df.iterrows():
            record = AuditingSummary(
                account_origin=row["account_origin"],
                suspect_count=int(row["suspect_count"]),
                total_amount=float(row["total_amount"])
            )
            session.add(record)
        session.commit()

        # Confirma inserção
        results = session.exec(select(AuditingSummary)).all()
        print(f"Foram inseridos {len(results)} registros.")

        if not results:
            RuntimeError("Nenhum registro carregado em auditing_summary")
        else:
            print("Exemplo de linha inserida:", results[0])