# models/models.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib #for saving large data and handling it faster - for optimizing slowness issue
from pathlib import Path
from typing import Union

class GameRecommender:

    #from the title.  The class keeps everything in instance attributes so
    #it can be reused without re‑instantiation.
    #reommends based on title, genre, ausing TF-IDF + cosine similarity
    
    def __init__(self, df: pd.DataFrame):
        # Normalise column names – strip, lower‑case
        df = df.copy()
        df.columns = df.columns.str.strip().str.lower()

        if "genres" in df.columns:
            df = df.rename(columns={"genres": "genre"})
        if "title" not in df.columns and "name" in df.columns:
            df = df.rename(columns={"name": "title"})

<<<<<<< HEAD

=======
>>>>>>> origin/feature/recommndation-imporvements
        #Pick the required column
        for col in["title", "genre"]:
            if col not in df.columns:
                raise ValueError(f"DataFrame must contain a '{col} column")

        #combine title, genre, and platform into one feature for the TF-IDF
        self.df = df.fillna("") #fill missing values
        self.df["combined"] = self.df["title"]+ " "+self.df["genre"]

        # Initialize the feature extractor & model (but *don't train yet*)
        self.vectorizer = TfidfVectorizer(max_features=3000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined"])

    #Using joblib to save/load better optimization
    def save(self, path: Union [str, Path]="game_recommender.pkl"):
        path = Path(path)
        joblib.dump({
            "vectorizer": self.vectorizer,
            "tfidf_matrix": self.tfidf_matrix,
            "df": self.df
        },path)
        print(f"Model saved to{path}")

    @staticmethod
    def load(path: Union [str, Path]= "game_recommender.pkl"):
        path = Path(path)
        data = joblib.load(path)
        obj = GameRecommender(data["df"])
        obj.vectorizer = data["vectorizer"]
        obj.tfidf_matrix = data["tfidf_matrix"]
        print(f"Model loaded from{path}")
        return obj

    def recommend(self, query: str, n:int = 5) -> str:
    #added int =5 so it recommends 5 games instead of just 1 at a time
    #Return a random title from the genre predicted for *query*.
        vec = self.vectorizer.transform([query.lower()])
        similarities = cosine_similarity(vec, self.tfidf_matrix).flatten()

    #getting top most n similar games
        top_idx = similarities.argsort()[-n:][::-1]
        top_games = self.df.iloc[top_idx]

    #to format the output
        formatted = "\n".join(
            f"{i+1}. {row['title'].title()} (Genre: {row['genre']})"
            for i, (_, row) in enumerate(top_games.iterrows())
        )
        return f"\nWe recommend: *{len(top_games)} game(s) matching your query:\n{formatted}"

