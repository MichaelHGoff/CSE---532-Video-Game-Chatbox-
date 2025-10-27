def preprocess_games(df):
    # Lowercase for consistency
    df['Title'] = df['Title'].str.lower()
    df['Genre'] = df['Genre'].str.lower()
    df['Platform'] = df['Platform'].str.lower()

    # Fill missing values
    df.fillna('', inplace=True)
    return df
