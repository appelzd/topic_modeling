
import gensim
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

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

    
    def create_lemmas_from_file(self, text, encoding='latin-1'):

        #Normalize
        text = text.lower()
      
        #Strip punctuation
        text = text.replace("'",'').replace("\n",' ')
        text = re.sub('[%s]' % re.escape(string.punctuation  + '£' + 'ï' + '»' + '¿'), ' ', text)
        
        # Tokenize
        # need to run commented line the first time you do this
        tokens = word_tokenize(text)
        tokens.append(getngrams(self,text))

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        stop_lambda = lambda x: [y for y in x if not y.isdigit() and y not in stop_words]
        tokens = stop_lambda(tokens ) 

        #Part of Speech
        # need to run commented line the first time you do this
        pos_lambda = lambda x: nltk.pos_tag(x)
        pos_wordnet = lambda x: [(y[0], get_wordnet_pos(y[1])) for y in x if get_wordnet_pos(y[1]) not None]
        speech_parts = pos_wordnet(pos_lambda(tokens))
        
        #Lemmatization
        lemmatizer = WordNetLemmatizer()
        lemmatizer_fun = lambda x: lemmatizer.lemmatize(*x)
        lemmas = [lemmatizer_fun(x) for x in speech_parts]
        
        return(lemmas)

        
    def getngrams(self, data):
        #for now, we are just getting bigrams (2 word phrases)
        #get sentences
        sentences = sent_tokenize(data)[0].split('\r')
        #foreach sentence, create bigram matrix with nltk.ngram
        ngramslist = []
        [ngramslist.append(ngrams(bi.lower().split(), 2)) for bi in sentences]

        #foreach bigram in bigram matrix
        #compare to our model to see if the biagram is a 'valid' phrase
        #if the phrase is valid, add it to the dictionary of terms
        rtn = []
        for gen in ngramslist:
            bg = [ '%s_%s' % (b[0], b[1]) for b in gen]
            rtn.append([word for word in i2w for w in bg if word.lower()==w])

        return rtn


    if __name__ == "__main__":
        pass


