import pickle

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

    def save_results(self, results, output_fname):
        with open(output_fname, "wb") as filehandle:
            pickle.dump(results, filehandle)
