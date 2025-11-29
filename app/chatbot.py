import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)
import os, sys
import random
import pandas as pd
from models.models import GameRecommender

#loads the cached CSV ('data/videogames.csv")
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

MODEL_PATH = os.path.join(project_root, "models", "game_recommender.pkl")
CSV_PATH = os.path.join(project_root, "data", "video_games.csv")

#----for small talk------
def detect_small_talk(query):
    #very simple small-ta;k recognition
    q = query.lower().strip()
    greeting =["hello", "hi", "hey", "greetings", "sup", "yo"]
    if any (word ==q for word in greeting):
        return random.choice([
            "Hey there! What kind of games do you like?",
            "Hi! Please tell me what game genre you're in the mood for",
            "Hello! Are you looking for something new to play?",
            "Greetings! Is there a specific type of game you were looking for?"
        ])
    if "how are you" in q:
        return random.choice([
            "I'm just a bunch of code, but I'm great! Thanks for asking. Looking for game recommendations?"
            "I am doing splendidly, I am ready to suggest game recommendations!"
            "Quite good, I love my job! Did you want a game recommendation?"
        ])
    if "thank" in q:
        return "You're welcome, glad I could be of help! Want another suggestion?"

    return None #Not small talk
#----------

#--more natural conversational replies----
def generate_reply(user_query, recommendation):
    #if recommendation is empty or unclear
    if not recommendation:
        fallback_response=[
            "Hmmm...I couldn't find a perfect match for that. Could you describe the type of game you're looking for?",
            "Sadly Nothing matched that search exactly. Please tell me a genre, mood, or game you like!",
            "I believe I might require a bit more detail. What style of game do you have in mind?"
        ]
        return random.choice(fallback_response)

    #choose lead-in based on query wording
    q = user_query.lower()
    if "similar" in q:
        lead_ins =[
            "If you are looking for something similar, try: ",
            "Here's a great alternative with a similar vibe:",
            "if you want something in the same spirit, I recommend: "
        ]
    elif "recommend" in q:
        lead_ins =[
            "Sure thing! I recommend: ",
            "Based on what you want, try this: ",
            "You might really enjoy this one: "
        ]
    else:
        lead_ins =[
            "Based on what you said you might enjoy: ",
            "I think this one fits your taste: ",
            "Here's something you might like: ",
            "You may want to check this out: "
        ]
    others = [
        "Want another recommendation?",
        "I can suggest more if you'd like!",
        "Let me know if you want something different",
        "Need more game ideas? Feel free to ask!"
    ]

    reply = (
        f"{random.choice(lead_ins)}\n"
        f"{recommendation}\n\n"
        f"{random.choice(others)}\n"
    )
    return reply
#-------------------

#main bot
#should be able to run this file directly to start a prompt loop
def main():
    #load dataset
    #changed csv_path = 'data/video_games.csv' to this (because of issues locating data file on my end):
    ##csv_path = os.path.join(project_root, 'data', 'video_games.csv')
    df = pd.read_csv(CSV_PATH)

    #for loading the trained if it exists saves, else train and save
    if os.path.exists(MODEL_PATH):
        bot = GameRecommender.load(MODEL_PATH)
    else:
        bot = GameRecommender(df)
        bot.save(MODEL_PATH)

    #intro
    print("\n🎮 Video‑Game Recommendation Bot")
    print("Tell me what kind of games you like! (Just Type 'quit' to exit.)")
    #prompt loop
    while True:
        query = input("\nYou: ").strip()
        if query.lower() in ("quit", "exit", "bye"):
            print("Bot: Goodbye! Have fun Gaming!")
            break

        #for small talk - simple answers
        small_talk_response = detect_small_talk(query)
        if small_talk_response:
            print("Bot: ", small_talk_response)
            continue

        #get recommendations - 5 recommendations
        try:
            result = bot.recommend(query, n=5)
        except Exception as e:
            result = f"Sorry, I couldn't find any games for your query. ({e})"

        #friendly formatting
        print("Bot: ", generate_reply(query, result))

if __name__ == "__main__":
    main()
    
