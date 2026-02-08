# Import Library
import pandas as pd
from sqlalchemy import create_engine
import os
# Creating the Loading Functions
def load_dream11_points(df: pd.DataFrame):
    # Warehouse DB connection details
    host = os.getenv("WH_DB_HOST")
    user = os.getenv("WH_DB_USER")
    password = os.getenv("WH_DB_PASSWORD")
    database = os.getenv("WH_DB_NAME")

    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}"
    )

    # Load DataFrame into warehouse
    df.to_sql(
        name="dream11_points_fact",
        con=engine,
        if_exists="replace",   # first time: replace
        index=False
    )

    print("Dream11 points table loaded into warehouse successfully")