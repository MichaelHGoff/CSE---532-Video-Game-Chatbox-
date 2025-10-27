#File to load Video game data from kaggle
import kagglehub, pandas as pd, os
from sqlalchemy import create_engine

def download_and_load():
    path = kagglehub.dataset_download("beridzeg45/video-games")
    csv_file = os.path.join(path, "games.csv")
    df = pd.read_csv(csv_file)
    engine = create_engine("sqlite:///videogames.db")
    df.to_sql("games", engine, if_exists="replace", index=False)
    return engine