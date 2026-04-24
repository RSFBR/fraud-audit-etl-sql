import pandas as pd
from sqlmodel import SQLModel, create_engine, Session, Field

class AuditingSummary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fraud_type: str
    count: int

def load_to_sql(csv_file="aggregated.csv", db_url="sqlite:///auditing.db"):
    df = pd.read_csv(csv_file)

    engine = create_engine(db_url)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for _, row in df.iterrows():
            record = AuditingSummary(fraud_type=row["transaction_id"], count=row["count"])
            session.add(record)
        session.commit()
    print("Registros inseridos em auditing_summary.")
