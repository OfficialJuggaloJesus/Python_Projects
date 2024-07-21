import numpy as np
from keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')

# Load Spacy for NER
nlp = spacy.load('en_core_web_sm')

# Load Keras model and resources
model = load_model('chatbot_model_tf.h5')
words = np.load('words.npy')
classes = np.load('classes.npy')

# Initialize Sentiment Analyzer
sid = SentimentIntensityAnalyzer()

def preprocess_text(sentence):
    # Remove punctuation
    sentence = re.sub(r'[^\w\s]', '', sentence)
    
    # Tokenize the sentence
    words = word_tokenize(sentence.lower())
    
    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    return words

def extract_entities(sentence):
    doc = nlp(sentence)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def predict_intent(model, sentence, words):
    sentence_words = preprocess_text(sentence)
    bow = [1 if word in sentence_words else 0 for word in words]
    bow = np.array(bow).reshape(1, -1)
    result = model.predict(bow)[0]
    
    # Filter out predictions below a threshold (e.g., 0.5)
    threshold = 0.5
    results = [[i, r] for i, r in enumerate(result) if r > threshold]
    
    # Sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    
    return return_list

def analyze_sentiment(sentence):
    sentiment = sid.polarity_scores(sentence)
    return sentiment

def chatbot_response(user_input):
    intents = predict_intent(model, user_input, words)
    intent = intents[0]  # Assuming the most probable intent
    
    # Example response based on intent
    if intent['intent'] == 'greeting':
        response = "Hello! How can I assist you today?"
    elif intent['intent'] == 'farewell':
        response = "Goodbye! Have a nice day."
    else:
        response = "I'm sorry, I didn't understand that."
    
    return response

# Example usage:
if __name__ == "__main__":
    user_input = input("You: ")
    response = chatbot_response(user_input)
    print("Bot:", response)
