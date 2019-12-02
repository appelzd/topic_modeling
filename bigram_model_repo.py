import gensim
import gensim.models.keyedvectors as word2vec

from PickleRepository import PickleRepo

class bigram_model_repo:

    modelId = 'pickled_bigram_model'
    target = None

    def getBigramModel(self):
        pickler = PickleRepo()

        model = pickler.GetPickledDoc(self.modelId, self.target)

        if model is not None:
            return model
        else:
            model=word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)  
            raw_model = model.wv.index2word
            model = self.gettrained_bigram_model(raw_model)
            pickler.SaveAsPickle(model, self.modelId, self.target)
            return model
  
    #todo need to move this to factory so we can have custom models for bigrams
    def gettrained_bigram_model(i2w):
        raw_list = list(filter(lambda s: '_' in s, i2w ))
        return [tup for tup in raw_list if len(raw_list)> 0]

