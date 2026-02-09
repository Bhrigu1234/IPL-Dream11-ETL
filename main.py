from src.extract import extract_raw_ball_data
from src.transform import transform_dream11_points
from src.load import load_dream11_points

def run_etl():
    print("Starting ETL pipeline...")

    raw_df = extract_raw_ball_data()
    print("Extraction done")

    dream11_df = transform_dream11_points(raw_df)
    print("Transformation done")

    load_dream11_points(dream11_df)
    print("Loading done")

if __name__ == "__main__":
    run_etl()
