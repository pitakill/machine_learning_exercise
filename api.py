import json
import numpy as np
import pickle
import random
import spacy

from keras.models import load_model

file_model = 'chatbot_model.h5'
data_json = 'intents.json'
words_file = 'words.pkl'
tags_file = 'tags.pkl'

model = load_model(file_model)
intents = json.loads(open(data_json).read())
words = pickle.load(open(words_file, 'rb'))
tags = pickle.load(open(tags_file, 'rb'))

npl = spacy.load('en_core_web_sm')

def clean_up_sentence(sentence):
    response = []
    for token in npl(sentence):
        if token.lemma_ != "-PRON-":
            response.append(token.lemma_.lower())
        else:
            response.append(token.text.lower())

    return response

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": tags[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

query = "Hello my friend"
print("We need to receive this in a json request: %s" % query)
print("We need to send this in a json response: %s" % chatbot_response(query))
