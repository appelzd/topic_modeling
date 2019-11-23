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
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import re
import string
from nltk import ngrams
import gensim.models.keyedvectors as word2vec

# our classes
import blobRepo
import Db
from PreprocessText import PlainTextPreprocessor

#!wget "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
model=word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)  
i2w = model.wv.index2word
        

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
    #dictionary.append(getbigram(lemmas))
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

def fit_new_doc(docfile, lda_model, dictionary):
    lemmas = create_lemmas_from_file(docfile)
    bow_corpus = dictionary.doc2bow(lemmas) 
    topic_prediction = lda_model.get_document_topics(bow_corpus)
    return(topic_prediction)
    
def writeToDb(topic):
    db = Db.Db()
    db.writeTopics(topic)
    
if __name__ == '__main__':
    
    lda_model, dictionary = PlainTextPreprocessor.identify_topics(PlainTextPreprocessor,num_topics=20, no_above=.95, no_below=.25)
    
    #topic_prediction = [fit_new_doc(file, lda_model, dictionary) for file in datafiles]
    
    for idx, topic in lda_model.print_topics(-1):
        print("Topic: {} ".format(idx))
        print("Word: {} ".format(topic))
        print("\n")
        writeToDb(topic)
        
    # for tp in topic_prediction:
    #     print('Test file likely to be topic {}, probability = {:.4f}'.format(tp[0][0], tp[0][1]))
    
    
















