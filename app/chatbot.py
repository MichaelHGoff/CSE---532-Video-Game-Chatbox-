import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

#loads the cached CSV ('data/videogames.csv")


import pandas as pd
from models.models import GameRecommender

#should be able to run this file directly to start a prompt loop
def main():
    #load dataset
    csv_path = 'data/video_games.csv'
    df = pd.read_csv(csv_path)

    #train the model
    bot = GameRecommender(df).train()

    #prompt loop 

    print("\n🎮 Video‑Game Recommendation Bot")
    print("Type a query.  Type 'quit' to exit.")
    while True:
        query = input("You: ").strip()
        if query.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        reply = bot.recommend(query)
        print("Bot:", reply)

if __name__ == "__main__":
    main()