import re
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

def cleanResume(documentText):
    documentText = re.sub('httpS+s*', ' ', documentText)  # remove URLs
    documentText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""), ' ', documentText)  # remove punctuations
    return documentText

def removeStopWords(words):
    words_new = []
    stopwords = nltk.corpus.stopwords.words('english')
    for word in words:
        if word not in stopwords:
            words_new.append(word)
    return words_new

def lemmatizeWords(words_new):
    wn = WordNetLemmatizer() 
    lem_words=[]
    for word in words_new:
        word=wn.lemmatize(word)
        lem_words.append(word)

    return lem_words