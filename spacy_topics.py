
import re
import gensim
import gensim.corpora as corpora
import gensim.utils as utils
from pathlib import Path
import os
import spacy
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')

stop_words = stopwords.words('english')
#stop_words.extend(['from', 'subject', 're', 'edu', 'use'])


def ldaModelize(lemmatized):
    id2words = corpora.Dictionary(lemmatized)
    corpus = [id2words.doc2bow(text) for text in lemmatized]

    return gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2words,
                                           num_topics=20, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)


def cleandata(datafiles):        
    processedFiles =  [processfiles(file) for file in datafiles]
    stopword_free = remove_stopwords(processedFiles)
    return [getbigram(doc) for doc in stopword_free]
    

def processfiles(file):
    with open(file, 'rt', encoding='utf-8') as fs:
        text = fs.read()

    text = text.lower()
    return gensim.utils.simple_preprocess(text, deacc=True)

def getbigram(data):
    bigram = gensim.models.phrases.Phrases(data, min_count=5, threshold=100)
    return gensim.models.phrases.Phraser(bigram)

def remove_stopwords(texts):
    return [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


if __name__ == '__main__':

    directory = r'C:\datafiles\exforge_008\d'
    
    datafiles = [os.path.join(directory, file.name) for file in Path(directory).iterdir()]

    cleaned_Files = cleandata(datafiles) 
    lemmatized = lemmatization(cleaned_Files, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    model = ldaModelize(lemmatized)

    for idx, topic in model.print_topics(-1):
        print("Topic: {} ".format(idx))
        print("Word: {} ".format(topic))
        print("\n")
