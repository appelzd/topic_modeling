import gensim
import re
import gensim.models.keyedvectors as word2vec
import string
from nltk.tokenize import sent_tokenize
from nltk import ngrams

import config
from PickleRepository import PickleRepo

class bigram_model_repo:

    modelId = 'pickled_bigram_model'
    target = None

    def getBigramModel(self):
        pickler = PickleRepo()
        _config = config.Configuration()
        target = _config.GetPickleRoot()
        
        model = pickler.GetPickledDoc(self.modelId, self.target)

        if model is not None:
            return model
        else:
            model=word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)  
            raw_model = model.wv.index2word
            model = self.gettrained_bigram_model(raw_model)
            pickler.SaveAsPickle(model, self.modelId, self.target)
            return model

    
    def getBigramList(self,data, bigram_model):
        #for now, we are just getting bigrams (2 word phrases)
        #get sentences
        sentences = sent_tokenize(data)
        #foreach sentence, create bigram matrix with nltk.ngram
        bigramsList = []
        for sent in sentences:
            cleaned_sent = re.sub('[%s]' % re.escape(string.punctuation  + '£' + 'ï' + '»' + '¿'), ' ', sent)
            split_sent = cleaned_sent.lower().split()

            temp = list(ngrams(split_sent,2))
            [bigramsList.append(t) for t in temp if t]

        return bigramsList
  
    #todo need to move this to factory so we can have custom models for bigrams
    def gettrained_bigram_model(self, i2w):
        raw_list = list(filter(lambda s: '_' in s, i2w ))
        return [tup for tup in raw_list if len(raw_list)> 0]

