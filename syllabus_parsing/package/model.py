

class Model:
    

    def preprocess(self, documents):
        pass

    def set_documents(self, documents):
        self.documents = documents
        self.preprocess(self.documents)

    def train(self, num_topics):
        pass

    def get_last_trained_results(self):
        pass
