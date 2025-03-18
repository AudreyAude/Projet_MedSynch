from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import spacy
nlp = spacy.load("en_core_web_sm")

# Créer un chatbot
chatbot = ChatBot(
    'MedicalChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation'
    ],
    database_uri='sqlite:///database.db'
)

# Entraînement avec les corpus de ChatterBot et un corpus médical spécifique si nécessaire
trainer = ChatterBotCorpusTrainer(chatbot)

# Entraînement de base avec des corpus généraux
trainer.train("chatterbot.corpus.french")  # Vous pouvez utiliser un corpus médical spécifique ici

# Fonction pour interagir avec le chatbot
def chat_with_bot():
    print("Bienvenue dans l'assistant médical virtuel ! Posez-moi une question.")
    while True:
        try:
            user_input = input("Vous: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("ChatBot: Au revoir! Prenez soin de vous.")
                break

            response = chatbot.get_response(user_input)
            print(f"ChatBot: {response}")
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

if __name__ == "__main__":
    chat_with_bot()
