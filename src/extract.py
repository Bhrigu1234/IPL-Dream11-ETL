# Import Library
import pandas as pd
from sqlalchemy import create_engine
import os
# Extraction Function

def extract_raw_ball_data(
    table_name: str = "raw_ipl_ball_by_ball"
) -> pd.DataFrame:

    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    if not all([host, user, password, database]):
        raise ValueError("Database environment variables are not set")

    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}"
    )

    query = f"SELECT * FROM {table_name}"

    df = pd.read_sql(query, engine)

    return df

if __name__ == "__main__":
    df = extract_raw_ball_data()
    print(df.head())
    print(f"Rows extracted: {len(df)}")