import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json

with open('intent.json') as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    # 'text' == text provided by user
    for pattern in intent["text"]:
        words_tokens = nltk.word_tokenize(pattern)
        words.extend(words_tokens) # words_tokens is already a list, use expend to like 'copy'
        docs_x.append(words_tokens)
        docs_y.append(intent["intent"])

    if intent["intent"] not in labels:
        labels.append(intent["intent"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
# set() - remove duplicate words
# list() - make it into list
# sorted - sort it
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    words_stem = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in words_stem:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)


tensorflow.compat.v1.reset_default_graph() 

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# For first time runner, u will encounter error at this line
# comment out all except model.fit() and model.save()
# after run 1 time, revert all code changes n you should be fine
# try:
#     model.load("./model/ai/model.tflearn")
# except:
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("./model/ai/model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

def chat(message):
    print("Start talking with the bot (type quit to stop)!")
    # while True:
    inp = str(message)

    results = model.predict([bag_of_words(inp, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['intent'] == tag:
            responses = tg['responses']

    message_to_send = random.choice(responses)
    return message_to_send
