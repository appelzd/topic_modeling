import unittest
import nltk
from nltk.corpus import wordnet
from  PreprocessText import PlainTextPreprocessor

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

    def test_gettokens_returnstokenlistwithoutpunc(self):
        results = PlainTextPreprocessor.gettokens(PlainTextPreprocessor, self.text)
        self.assertNotIn(['.', ','], results, 'contains punctuation')

    # bigrams is not working right now
    # def test_getbigramlist_returnslistinproperformat(self):
    #     results = PlainTextPreprocessor.getbigramlist(PlainTextPreprocessor, self.text)
        
    #     self.assertIn( ('add','which') ,results)    
    


if __name__ == "__main__":
    unittest.main()



