import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import numpy
import tflearn
import tensorflow
import random
import json

# Step 1: Prepare data

# Get all data from json file
with open('intent.json') as file:
    data = json.load(file)

# Google stem vs lemmatizer. Lemmatizer more suitable
lemmatizer = WordNetLemmatizer()
# List of words that given by user, and based on these words, trigger the 'intents' for bots
user_input_trigger_words = [] 
intents = []
docs_x = []
docs_y = []

# 
for intent in data["intents"]:
    # Get text from user input, that makes bot determine which intent it is
    for text in intent["text"]:
        words_tokens = nltk.word_tokenize(text)
        user_input_trigger_words.extend(words_tokens) # words_tokens is already a list, use expend to like 'copy'
        docs_x.append(words_tokens)
        docs_y.append(intent["intent"])

    if intent["intent"] not in intents:
        intents.append(intent["intent"])

# Apparently some word will be incorrectly stemmed
# there -> ther
# hola -> hol
user_input_trigger_words = [lemmatizer.lemmatize(w.lower()) for w in user_input_trigger_words if w.isalnum()]
# set() - remove duplicate user_input_trigger_words
# list() - make it into list
# sorted - sort it
user_input_trigger_words = sorted(list(set(user_input_trigger_words)))

intents = sorted(intents)


# Step 2: Prepare training data
training = []
output = []

out_empty = [0 for _ in range(len(intents))]

for x, doc in enumerate(docs_x):
    bag = []

    words_lammatized = [lemmatizer.lemmatize(w.lower()) for w in doc]

    for w in user_input_trigger_words:
        if w in words_lammatized:
            bag.append(1)
        else:
            bag.append(0)
    # By using the slicing notation [:], a new list is created with the same elements as out_empty, 
    # effectively making a shallow copy of the list. This means that modifying output_row will not affect the 
    # original list out_empty.
    # Using the slicing notation to create a copy of a list is a common way to avoid modifying the original 
    # list when you need a new list with the same elements. It ensures that you have a separate list object 
    # with the same values as the original list.
    output_row = out_empty[:]
    # x = 0
    # docs_y[0] = 'greetings'
    # intents.index('greetings') == 7
    output_row[intents.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)

# Step 3: Train model
# Reset graph
tensorflow.compat.v1.reset_default_graph() 

# Neural Network
net = tflearn.input_data(shape=[None, len(training[0])]) # layer 1 - input layer
net = tflearn.fully_connected(net, 8) # layer 2 - hidden layer
net = tflearn.fully_connected(net, 8) # layer 3 - hidden layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") # last layer - output layer
net = tflearn.regression(net)

model = tflearn.DNN(net)

# For first time runner, u will encounter error at this line
# comment out all except model.fit() and model.save()
# after run 1 time, revert all code changes n you should be fine
try:
    model.load("./model/ai/model.tflearn")
except:
    # Train model (?)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    # Save model
    model.save("./model/ai/model.tflearn")


def bag_of_words(s, user_input_trigger_words):
    bag = [0 for _ in range(len(user_input_trigger_words))]

    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(user_input_trigger_words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

# Main function - call this to start chatting
def chat(message):
    inp = message.content

    results = model.predict([bag_of_words(inp, user_input_trigger_words)])
    results_index = numpy.argmax(results)
    tag = intents[results_index]
    print(tag)

    for tg in data["intents"]:
        if tg['intent'] == tag:
            responses = tg['responses']

    message_to_send = random.choice(responses)
    return message_to_send
