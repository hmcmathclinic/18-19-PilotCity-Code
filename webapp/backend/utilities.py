import numpy
import argparse


class Utils:

    def __init__(self):
        fp = open("glove.6B.100d.npy", "rb")
        self.wordL, self.array, self.lengths = self.load_glove_vectors(fp)
        self.index_dict = {} # keys: words, values: index
        for i in range(len(self.wordL)):
            self.index_dict[self.wordL[i]] = i

    def load_text_vectors(self, f):
        ''' loads vectors from text file, returning
        an array of vectors and a list of words each index 
        of aray corresponds to '''
        wordL = []
        num_rows = 0
        for line in f.readlines():
            vector = line.split(" ")
            # determine the number of columns in the array
            num_columns = len(vector) - 1
            num_rows += 1
            # determine the number of rows in the array

        # create an array filled with zeros that has the right number of rows and columns
        array = numpy.zeros((num_rows, num_columns))
        f.seek(0) # get back to the start
        # for each row in the GloVe file:
        i = 0
        for line in f.readlines():
            vector = line.split(" ")
            word = vector[0]
            wordL.append(word)
            vector = vector[1:]
            # fill the appropriate array row with the GloVe file row
            array[i] = list(map(float, vector))
            i += 1

        return wordL, array

    def save_glove_vectors(self, wordL, array, fp):
        ''' Saves the list of words and their corresponding
        vectors to the npy file fp is pointing to'''
        numpy.save(fp, array)      # the numpy array returned by your load_text_vectors function    
        numpy.save(fp, wordL)      # the list of words returned by your load_text_vectors function
        numpy.save(fp, self.compute_lengths(array)) # lengths of each vector
        fp.close()

    def load_glove_vectors(self, fp):
        '''Loads the npy file fp is pointing to, returning 
        the word list, array, and vector lengths fp contains'''
        array = numpy.load(fp)
        wordL = list(numpy.load(fp))
        lengths = numpy.load(fp) # how to make sure that this is different from wordL!!??
        fp.close()
        return wordL, array, lengths

    def compute_lengths(self, array):
        ''' takes the array as its only parameter and returns a 
        new array that stores the lengths of each row in the array. '''
        return numpy.linalg.norm(array, axis=1)

    def get_vec(self, word):
        ''' Given a certain word we want to find within
        a list of words, corresponding vector array,
        and corresponding vector lengths, returns a
        tuple containing the vector of that word and
        the length of that vector  '''    # see what is taking all the time tho
        word_index = self.index_dict[word] 
        word_vector = self.array[word_index]
        word_length = self.lengths[word_index]
        return word_vector, word_length

    def cosine_similarity(self, vec1, vec2, lens1, lens2):
        ''' Takes in 2 vectors and their lengths. 
        Returns their cosine similarity. '''
        dot_product = numpy.dot(vec1, vec2)
        return dot_product / (lens1 * lens2)

    def score(self, w1, w2):
        if w1 not in self.wordL or w2 not in self.wordL:
            return 2
        w1_vector, w1_len = self.get_vec(w1)
        w2_vector, w2_len = self.get_vec(w2)
        return self.cosine_similarity(w1_vector, w2_vector, w1_len, w2_len)
    
    
