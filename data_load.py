#File to load Video game data from kaggle
import os
import pandas as pd
import kagglehub

# Folder to store dataset locally
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Name of your CSV file (adjust if needed)
CSV_FILENAME = "video_games.csv"
CSV_PATH = os.path.join(DATA_DIR, CSV_FILENAME)

# Function to load dataset
def load_dataset():
    if os.path.exists(CSV_PATH):
        print(f"Loading dataset from local file: {CSV_PATH}")
        df = pd.read_csv(CSV_PATH)
    else:
        print("Local CSV not found. Downloading from Kaggle...")
        dataset_path = kagglehub.dataset_download("beridzeg45/video-games")
        csv_files = [f for f in os.listdir(dataset_path) if f.endswith(".csv")]
        if not csv_files:
            raise FileNotFoundError("No CSV file found in the downloaded Kaggle dataset")
        # Save the first CSV locally
        df = pd.read_csv(os.path.join(dataset_path, csv_files[0]))
        df.to_csv(CSV_PATH, index=False)
        print(f"Dataset saved locally at: {CSV_PATH}")
    return df

# Load dataset
df = load_dataset()
print(df.head())
