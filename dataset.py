import pandas as pd

file_path = 'games.csv'

# Try reading the file flexibly (tab or comma)
df = pd.read_csv(file_path, sep=None, engine='python')

# Show the actual column names
print("Columns in file:", df.columns.tolist())

# If 'Title' has spaces or invisible chars, clean them up:
df.columns = df.columns.str.strip()

# Try accessing it again
game_titles = df['Title']
print(game_titles)
