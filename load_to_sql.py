import pandas as pd
from sqlmodel import SQLModel, create_engine, Session, Field

# class AuditingSummary(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     fraud_type: str
#     count: int

# def load_to_sql(csv_file="interim/aggregated.csv", db_url="sqlite:///auditing.db"):
#     df = pd.read_csv(csv_file)
#     print(df.head())  # Verifica os dados antes de carregar
#     print(df.columns)  # Verifica os nomes das colunas

#     # Renomeia a primeira coluna para "fraud_type"
#     first_col = df.columns[0]
#     df = df.rename(columns={first_col: "fraud_type"})

#     engine = create_engine(db_url)
#     SQLModel.metadata.create_all(engine)

#     with Session(engine) as session:
#         for _, row in df.iterrows():
#             record = AuditingSummary(fraud_type=row["fraud_type"], count=row["count"])
#             session.add(record)
#         session.commit()
#     print("Registros inseridos em auditing_summary.")

class AuditingSummary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_origin: str
    suspect_count: int
    total_amount: float

def load_to_sql(csv_file="interim/aggregated.csv", db_url="sqlite:///auditing.db"):
    df = pd.read_csv(csv_file)
    print(df.head())
    print(df.columns)

    engine = create_engine(db_url)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for _, row in df.iterrows():
            record = AuditingSummary(
                account_origin=row["account_origin"],
                suspect_count=row["suspect_count"],
                total_amount=row["total_amount"]
            )
            session.add(record)
        session.commit()
    print("Registros inseridos em auditing_summary.")