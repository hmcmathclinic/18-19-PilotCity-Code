

class Model:

    def __init__(self, bag_of_words):
        self.bag_of_words = bag_of_words
    
    def get_bag_of_words(self):
        return self.bag_of_words
    
    def set_bag_of_words(self, bag_of_words):
        self.bag_of_words = bag_of_words

    def train(self):
        pass
