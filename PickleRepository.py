import pickle
import os
from config import Configuration

class PickleRepo:

    def SaveAsPickle(self, document, documentId, target=None):
        path = self.GetPath(target)
    
        #create non-exisitng path
        if not os.path.exists(path):
            os.makedirs(path)

        # Make sure that the parent is a directory and not a file
        if not os.path.isdir(path):
            raise ValueError(
                "Please supply a directory to write preprocessed data to."
            )
        
        try:
            with open(os.path.join(path, str(documentId)), 'wb') as f:
                pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print('exception pickling doc')
            print(e)

    
    def GetPickledDoc(self, documentId, target=None):
        path = self.GetPath(target)

        with open(os.path.join(path, str(documentId)), 'rb') as f:
            return pickle.load(f)


    def GetPath(self,target=None):
        if target == None:
            path = Configuration.GetPickleRoot()
        else:
            path = target
    
        return path
