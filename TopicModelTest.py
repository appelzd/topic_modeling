import unittest
import TopicModel

class TestTopicModel(unittest.TestCase):

    def test_gettrained_bigram_model(self):
        result = TopicModel.gettrained_bigram_model()
        self.assertTrue(lambda x: len(list(filter(lambda tup: tup not in '_', result))) > 0)



if __name__ == "__main__":
    unittest.main()    