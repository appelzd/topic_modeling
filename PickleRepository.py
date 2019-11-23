import pickle
import os
from config import Configuration

class PickleRepo:

    def SaveAsPickle(self, document, target=None):
        path = self.GetPath(target)
    
        #create non-exisitng path
        if not os.path.exists(path):
            os.makedirs(path)

        # Make sure that the parent is a directory and not a file
        if not os.path.isdir(parent):
            raise ValueError(
                "Please supply a directory to write preprocessed data to."
            )
        
        try:
            with open(path, 'wb') as f:
                pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print('exception pickling doc')
            print(e)

    
    def GetPickledDoc(self, documentName, target=None):
        path = self.GetPath(target)

        with open(path, 'rb') as f:
            pickle.load(f)


    def GetPath(target=None):
        if target == None:
            path = Configuration.GetPickleRoot()
        elif
            path = target
    
        return path
