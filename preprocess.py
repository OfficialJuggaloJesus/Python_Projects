import json
import numpy as np
import random
import nltk
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load the intents file
intents = json.loads(open('intents.json').read())

# Initialize lists to hold words, classes, and documents
words = []
classes = []
documents = []
ignore_words = ['?', '!']

# Process each intent in the intents file
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word in the sentence
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        # Add the tokenized sentence and the corresponding tag to documents
        documents.append((word_list, intent['tag']))
        # Add the tag to classes if it's not already there
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and lower each word, and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(set(words))

# Sort classes
classes = sorted(set(classes))

# Print words and classes for verification
print(words)
print(classes)

# Create the training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])

# Shuffle the training data
random.shuffle(training)
training = np.array(training, dtype=object)

# Split the training data into patterns (train_x) and intents (train_y)
train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

# Save the preprocessed data to files for later use
np.save('train_x.npy', train_x)
np.save('train_y.npy', train_y)
np.save('words.npy', words)
np.save('classes.npy', classes)

print("Data preprocessing completed and saved to files.")
