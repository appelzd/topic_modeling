import unittest
import nltk;

from PickleRepository import PickleRepo

class TestPickleRepo(unittest.TestCase):

    testDoc = 'Once upon a time, long long ago . . .'
    target = './test_pickles'
    documentId = 1123

    def test_saveAsPickle(self):
        try:
            repo = PickleRepo()
            repo.SaveAsPickle(self.testDoc, self.documentId, self.target)
            self.assertTrue(1==1)
        except Exception as e:
            self.assertIsNone(e)

    # def test_getPickle(self):
    #     repo = PickleRepo()
    #     doc = repo.GetPickledDoc('testDoc', target)
    #     self.assertTrue(doc != None)

if __name__ == "__main__":
    unittest.main()
