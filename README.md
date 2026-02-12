# IPL-Dream11-ETL
End-to-end ETL transformation pipeline to compute Dream11-style fantasy points from IPL ball-by-ball data

## 📌 Project Overview
This project implements an end-to-end ETL (Extract, Transform, Load) pipeline using IPL ball-by-ball data to calculate Dream11 fantasy points for each player per match.

The goal of this project is to demonstrate real-world data engineering practices including data extraction from a database, transformation using business logic, and loading into a data warehouse.

---

## 🏗️ Architecture Overview

Source → Transform → Warehouse

- **Extract**: Raw IPL ball-by-ball data extracted from MySQL (AWS RDS)
- **Transform**: Player-wise batting, bowling, and fielding points calculated using Dream11 scoring rules
- **Load**: Final Dream11 points table loaded into a warehouse database

## 📂 Project Structure

```
IPL-Dream11-ETL/
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── outputs/
│   └── dream11_points.csv
│
├── notebooks/
├── requirements.txt
└── README.md
```


## 🛠️ Tech Stack

- Python
- Pandas
- MySQL
- SQLAlchemy
- AWS RDS
- Git & GitHub

## 📊 Transformation Logic (Highlights)

- Batting points: runs, fours, sixes, strike rate bonuses
- Bowling points: wickets, maidens, economy rate, dot balls
- Fielding points: catches, run-outs, stumpings
- Final Dream11 score calculated per player per match

## 🔐 Data Handling

- Raw data is stored locally or in AWS RDS
- Raw CSV files are not committed to GitHub due to size and security reasons
- Folder structure is maintained using `.gitkeep`

## ▶️ How to Run

1. Set database environment variables:
   - DB_HOST
   - DB_USER
   - DB_PASSWORD
   - DB_NAME

2. Run extraction:
   python src/extract.py

3. Run extraction:
    python src/transform.py

4. Run load:
    python src/load.py

