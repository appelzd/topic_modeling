import unittest
import nltk
from nltk.corpus import wordnet
from  PreprocessText import PlainTextPreprocessor
from bigram_model_repo import bigram_model_repo as bigRepo

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

class PreprocessorTest(unittest.TestCase):

    text = 'Next, we add a tokenize() method to our Preprocessor, which, given a raw document, will perform segmentation, tokenization, and part-of-speech tagging using the NLTK methods we explored in the previous section. This method will return a generator of paragraphs for each document that contains a list of sentences, which are in turn lists of part-of-speech tagged tokens'

    def test_getPartofSpeechTagging_returnsNoun(self):
        tagged = nltk.pos_tag(self.text.split()) 

        result = PlainTextPreprocessor.get_wordnet_pos(PlainTextPreprocessor, tagged[8][1])      

        self.assertEqual(wordnet.NOUN, result)

    def test_getPartofSpeechTagging_returnsVerb(self):
        tagged = nltk.pos_tag(self.text.split()) 

        result = PlainTextPreprocessor.get_wordnet_pos(PlainTextPreprocessor, tagged[2][1])

        self.assertEqual(wordnet.VERB, result)

    def test_getPartofSpeechTagging_returnsNone(self):
        tagged = nltk.pos_tag(self.text.split()) 

        result = PlainTextPreprocessor.get_wordnet_pos(PlainTextPreprocessor, tagged[3][1])

        self.assertEqual(None, result)


    def test_getPartsofSpeech_returnsNoun(self):
        tokens = ['desk'] 

        result = PlainTextPreprocessor.getPartsofSpeech(PlainTextPreprocessor, tokens)      

        self.assertEqual(wordnet.NOUN, result[0][1])

    def test_getPartsofSpeech_returnsVerb(self):
        tokens = ['swimming']

        result = PlainTextPreprocessor.getPartsofSpeech(PlainTextPreprocessor, tokens)

        self.assertEqual(wordnet.VERB, result[0][1])

    def test_getPartsofSpeech_returnsNone(self):
        tokens = ['we']

        result = PlainTextPreprocessor.getPartsofSpeech(PlainTextPreprocessor, tokens)

        self.assertEqual(None, result[0][1])


    def test_gettokens_returnstokenlistwithoutpunc(self):
        results = PlainTextPreprocessor.getTokens(PlainTextPreprocessor, self.text)
        self.assertNotIn(['.', ','], results, 'contains punctuation')

    def test_removestopwords_returnstokenlistwithoutstopwords(self):
        tokens = PlainTextPreprocessor.getTokens(PlainTextPreprocessor, self.text)
        results = PlainTextPreprocessor.removeStopWords(PlainTextPreprocessor, tokens)
        self.assertNotIn(['and', 'a'], results, 'contains stopwords')
    

    def test_getbigramlist_returnslistinproperformat(self):
        repo = bigRepo()
        results = repo.getBigramList(self.text, [])
        
        self.assertIn(('which', 'given') ,results)    
    
    def test_getbigram_returns(self):
        repo = bigRepo()
        tokens = repo.getBigramList(self.text, [])
        
        trained_bigram_model = ['which_given', 'lake_michigan', 'nltk_methods']
        results = PlainTextPreprocessor.getNGrams(PlainTextPreprocessor, tokens, trained_bigram_model)

        self.assertIn(('which_given') ,results)    
        self.assertIn(('nltk_methods') ,results)    
        self.assertNotIn(('lake_michigan'), results)


if __name__ == "__main__":
    unittest.main()



