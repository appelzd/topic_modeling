import sys
import os
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import ngrams
import gensim.models.keyedvectors as word2vec
from pathlib import Path

#nlp = spacy.load('en_core_web_lg')
model=word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)  
i2w = model.wv.index2word


if __name__ == '__main__':
    #hard-coded so examples can be easily swapped
    directory = r'C:\datafiles\exforge_008\d'
    file = [os.path.join(directory, file.name) for file in Path(directory).iterdir()]

    with open(file[0], 'rt') as f:
        text = f.read()

    #get sentences
    sentences = sent_tokenize(text)[0].split('\r')
    #foreach sentence, create bigram matrix with nltk.ngram
    ngramslist = []
    [ngramslist.append(ngrams(bi.lower().split(), 2)) for bi in sentences]

    rtn = []
    for gen in ngramslist:
        bg = [ '%s_%s' % (b[0], b[1]) for b in gen]
        rtn.append([word) for word in i2w for w in bg if word.lower()==w]])    

    f = rtn

    



