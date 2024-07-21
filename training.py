import numpy as np
import random
from nltk.stem import WordNetLemmatizer
import json

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load the preprocessed data
with open('intents.json') as file:
    intents = json.load(file)

words = np.load('words.npy').tolist()
classes = np.load('classes.npy').tolist()

# Initialize lists to hold the training data
training = []
output_empty = [0] * len(classes)

# Process each document in the intents data
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize and lemmatize each word in the sentence
        word_list = nltk.word_tokenize(pattern)
        word_list = [lemmatizer.lemmatize(word.lower()) for word in word_list]
        
        # Create a bag of words
        bag = [1 if word in word_list else 0 for word in words]
        
        # Create the output vector
        output_row = list(output_empty)
        output_row[classes.index(intent['tag'])] = 1
        
        # Append the BoW and output vector to training data
        training.append([bag, output_row])

# Shuffle the training data
random.shuffle(training)
training = np.array(training, dtype=object)

# Split the training data into patterns (train_x) and intents (train_y)
train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

# Save the training data for later use
np.save('train_x.npy', train_x)
np.save('train_y.npy', train_y)

print("Training data created and saved to files.")
