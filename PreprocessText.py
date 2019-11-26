
import gensim
import os
import nltk
import re
import string
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import gensim.models.keyedvectors as word2vec

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

class PlainTextPreprocessor:

    def get_wordnet_pos(self, treebank_tag):
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
            return None
    

    def getTokens(self, text):
        #Normalize
        text = text.lower()
      
        #Strip punctuation
        text = text.replace("'",'').replace("\n",' ')
        text = re.sub('[%s]' % re.escape(string.punctuation  + '£' + 'ï' + '»' + '¿'), ' ', text)
        
        # Tokenize
        # need to run commented line the first time you do this
        tokens = word_tokenize(text)
        #tokens.append(self.getngrams(text))
        return tokens

    def removeStopWords(self, tokens):
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        stop_lambda = lambda x: [y for y in x if not y.isdigit() and y not in stop_words]
        return stop_lambda(tokens ) 

    def getPartsofSpeech(self, tokens):
        #Part of Speech
        pos_lambda = lambda x: nltk.pos_tag(x)
        pos_wordnet = lambda x: [(y[0], self.get_wordnet_pos(self, y[1])) for y in x]
        return pos_wordnet(pos_lambda(tokens))

    def getLemmas(self, speech_parts):        
        #Lemmatization
        lemmatizer = WordNetLemmatizer()
        lemmatizer_fun = lambda x: lemmatizer.lemmatize(*x)
        lemmas = [lemmatizer_fun(x) for x in speech_parts]
        
        return(lemmas)

    def getBigramList(self,data):
        #for now, we are just getting bigrams (2 word phrases)
        #get sentences
        sentences = sent_tokenize(data)
        #foreach sentence, create bigram matrix with nltk.ngram
        bigramsList = []
        for sent in sentences:
            cleaned_sent = re.sub('[%s]' % re.escape(string.punctuation  + '£' + 'ï' + '»' + '¿'), ' ', sent)
            split_sent = cleaned_sent.lower().split()
            temp = list(ngrams(split_sent,2))
            [bigramsList.append(t) for t in temp]

        return bigramsList
        
    def getNGrams(self, data, trained_bigram_model):
        
        #foreach bigram in bigram matrix
        #compare to our model to see if the biagram is a 'valid' phrase
        #if the phrase is valid, add it to the dictionary of terms
        rtn = []
        for gen in data:
            bg = '%s_%s' % (gen[0], gen[1])
            result = (list(filter( lambda d: d==bg, trained_bigram_model)))
            [rtn.append(r) for r in result if len(result) > 0]

        return rtn




