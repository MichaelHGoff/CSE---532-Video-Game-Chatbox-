# models/models.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from typing import Iterable



class GameRecommender:
    
    #Train a TF‑IDF → RandomForest classifier that predicts a game genre
    #from the title.  The class keeps everything in instance attributes so
    #it can be reused without re‑instantiation.
    
    def __init__(self, df: pd.DataFrame):
        # Normalise column names – strip, lower‑case
        df = df.copy()
        df.columns = df.columns.str.strip().str.lower()

        #Pick the first column that looks like a title / name
        title_col = next((c for c in df.columns
                          if 'title' in c or 'name' in c), None)
        #Pick the genre column
        genre_col = next((c for c in df.columns if 'genre' in c), None)

        if title_col is None or genre_col is None:
            raise ValueError(
                "Input DataFrame must contain a ‘title’ (or 'name') "
                "and a ‘genre’ column"
            )

        #Keep only those columns, rename to canonical names,
        # and drop rows missing either value
        df = df[[title_col, genre_col]].rename(
            columns={title_col: 'title', genre_col: 'genre'}
        ).dropna(subset=['title', 'genre'])

        self.df = df

        # Initialize the feature extractor & model (but *don't train yet*)
        self.vectorizer = TfidfVectorizer(max_features=2000)
        self.model = RandomForestClassifier(
            n_estimators=200, random_state=42
        )

    def train(self) -> "GameRecommender":
        
        #Fit the TF‑IDF vectorizer & RandomForest on the dataset.
        #Returns self to allow chaining:  recommender.train()
        
        X = self.vectorizer.fit_transform(self.df['title'])
        y = self.df['genre']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model.fit(X_train, y_train)
        acc = self.model.score(X_test, y_test)
        print(f" Model accuracy: {acc*100:.1f}%")
        return self

    def recommend(self, query: str) -> str:
       
        #Return a random title from the genre predicted for *query*.
        
        vec = self.vectorizer.transform([query.lower()])
        genre = self.model.predict(vec)[0]
        candidate = self.df[self.df['genre'] == genre].sample(1)['title'].iloc[0]
        return f"We recommend: *{candidate.title()}* (Genre: {genre})"
