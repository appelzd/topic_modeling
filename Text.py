# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:20:46 2019

@author:  Scott Schafer
@date:    8/5/2019
@purpose: fundamental text mining functions
"""

import gensim
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import re
import string
from pathlib import Path
from nltk import ngrams
import gensim.models.keyedvectors as word2vec
import spacy

# our classes
import blobRepo
import Db

#!wget "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
#model=word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)  

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

nlp = spacy.load('en_core_web_lg')    

def get_wordnet_pos(treebank_tag):
    # Convert the naming scheme to that recognized by WordNet
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    
def create_lemmas_from_file(text, encoding='latin-1'):

        #Normalize
        text = text.lower()
      
        #Strip punctuation
        text = text.replace("'",'').replace("\n",' ')
        text = re.sub('[%s]' % re.escape(string.punctuation  + '£' + 'ï' + '»' + '¿'), ' ', text)
        
        # Tokenize
        # need to run commented line the first time you do this
        tokens = word_tokenize(text) 
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        stop_lambda = lambda x: [y for y in x if y not in stop_words]
        tokens = stop_lambda(tokens ) 

        #Part of Speech
        # need to run commented line the first time you do this
        pos_lambda = lambda x: nltk.pos_tag(x)
        pos_wordnet = lambda x: [(y[0], get_wordnet_pos(y[1])) for y in x]
        speech_parts = pos_wordnet(pos_lambda(tokens))
        
        #Lemmatization
        lemmatizer = WordNetLemmatizer()
        lemmatizer_fun = lambda x: lemmatizer.lemmatize(*x)
        lemmas = [lemmatizer_fun(x) for x in speech_parts]
        
        return(lemmas)
        

def identify_topics(num_topics=5, no_below=3, no_above=.34, passes=50):
    #create topics based on lemma lists created from whole files
    
    lemmas = []
    for datafile in blobRepo.BlobRepo.GetBlobs(blobRepo.BlobRepo):
        try:
            lemmas.append(create_lemmas_from_file(datafile))                
        except Exception as e :
            print(e)
            continue

    #create and filter dictionary
    dictionary = gensim.corpora.Dictionary(lemmas)
    dictionary.filter_extremes(no_below=no_below, 
                               no_above=no_above)
    
    #Use dictionary to form bag of words
    bow_corpus = [dictionary.doc2bow(doc) for doc in lemmas]
    
    #Fit tfidf model
    tfidf = gensim.models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]
    lda_model_tfidf = gensim.models.LsiModel(corpus_tfidf, 
                                             #num_topics=num_topics, 
                                             id2word = dictionary 
                                             #passes = passes
                                             )
    return(lda_model_tfidf, dictionary)

def getbigram(data):
    i2w = model.wv.index2word
    bigrams = list(ngrams(data.split(), 2))
    bg = [ '%s_%s' % (b[0], b[1]) for b in bigrams]
    return [word for word in i2w for w in bg if word.lower()==w]

def fit_new_doc(docfile, lda_model, dictionary):
    lemmas = create_lemmas_from_file(docfile)
    bow_corpus = dictionary.doc2bow(lemmas) 
    topic_prediction = lda_model.get_document_topics(bow_corpus)
    return(topic_prediction)
    
def writeToDb(topic):
    db = Db.Db()
    db.writeTopics(topic)
    
if __name__ == '__main__':
    
    #hard-coded so examples can be easily swapped
    # directory = r'C:\datafiles\exforge_008\d'
    
    # datafiles = [os.path.join(directory, file.name) for file in Path(directory).iterdir()]
    lda_model, dictionary = identify_topics(num_topics=20, no_above=.95, no_below=.25)
    
    #topic_prediction = [fit_new_doc(file, lda_model, dictionary) for file in datafiles]
    
    for idx, topic in lda_model.print_topics(-1):
        print("Topic: {} ".format(idx))
        print("Word: {} ".format(topic))
        print("\n")
        writeToDb(topic)
        
    # for tp in topic_prediction:
    #     print('Test file likely to be topic {}, probability = {:.4f}'.format(tp[0][0], tp[0][1]))
    
    
















