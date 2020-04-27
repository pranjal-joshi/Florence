
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import numpy as np

f = open('nltk.txt','r',errors='ignore')
t = f.read()
t = t.replace('\n','').lower()
f.close()

st = nltk.sent_tokenize(t)
wt = nltk.word_tokenize(t)

lemmer = nltk.stem.WordNetLemmatizer()

def lemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punc_dict = dict((ord(punc),None) for punc in string.punctuation)

def lemNormalize(text):
    return lemTokens(nltk.word_tokenize(text.lower().translate(remove_punc_dict)))

def response(input):
    st.append(input)
    tv = TfidfVectorizer(tokenizer=lemNormalize,stop_words='english')
    tfidf = tv.fit_transform(st)
    vals = cosine_similarity(tfidf[-1],tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfdif = flat[-2]

    if req_tfdif == 0:
        print("Response Error: Don't understand")
    else:
        print("\nANSWER: " + st[idx])

response("who is jarvis?")