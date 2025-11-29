from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

#Initializing Chatbot
chatbot = ChatBot("Video-Game Chatbot")
trainer = ChatterBotCorpusTrainer(chatbot)

#to train chatbot with English data so it speaks english
trainer.train("chatterbot.corpus.english")

#Loop for chat - chat will continue as long as it is true
print("Welcome! Type anything to start the conversation with our Video-Game Recommendation Chatbot.")
while True:
    user_input = input("You: ") #want to add the ability for person to update with their name?
    response = chatbot.get_response(user_input)
    print("Video-Game Chatbot:", response)

#needs a way to exit chatbot
    # print("You have Chosen to leave conversation....")
    #print("You left the conversation")
    print("")



