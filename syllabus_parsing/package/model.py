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
    
    def transform_unseen_document(self, document):
        pass
    
    def extract_topics_from_trained_model(self, trained_model, num_topics):
        pass

    def get_last_trained_results(self):
        return self.last_trained_results

    def set_trained_model(self, trained_model):
        self.trained_model = trained_model

    def get_trained_model(self):
        return self.trained_model

    @staticmethod
    def save_info(info, output_fname):
        with open(output_fname, "wb") as filehandle:
            pickle.dump(info, filehandle)

    @staticmethod
    def load_saved_info(fname):
        return pickle.load(open(fname, "rb" ))