import pickle

class Model:
    
    def __init__(self):
        self.last_trained_results = None
        self.trained_model = None

    def preprocess(self, documents):
        pass

    def set_documents(self, documents):
        self.documents = documents
        self.preprocess(self.documents)

    def train(self, num_topics, use_tfidf=False):
        pass

    def get_last_trained_results(self):
        return self.last_trained_results

    def get_trained_model(self):
        return self.trained_model

    def save_results(self, results, output_fname):
        with open(output_fname, "wb") as filehandle:
            pickle.dump(results, filehandle)
