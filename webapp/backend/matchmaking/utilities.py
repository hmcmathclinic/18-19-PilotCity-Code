
import numpy
import argparse

def load_text_vectors(f):
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

def save_glove_vectors(wordL, array, fp):
    ''' Saves the list of words and their corresponding
    vectors to the npy file fp is pointing to'''
    numpy.save(fp, array)      # the numpy array returned by your load_text_vectors function    
    numpy.save(fp, wordL)      # the list of words returned by your load_text_vectors function
    numpy.save(fp, compute_lengths(array)) # lengths of each vector
    fp.close()

def load_glove_vectors(fp):
    '''Loads the npy file fp is pointing to, returning 
    the word list, array, and vector lengths fp contains'''
    array = numpy.load(fp)
    wordL = list(numpy.load(fp))
    lengths = numpy.load(fp) # how to make sure that this is different from wordL!!??
    fp.close()
    return wordL, array, lengths

def compute_lengths(array):
    ''' takes the array as its only parameter and returns a 
    new array that stores the lengths of each row in the array. '''
    return numpy.linalg.norm(array, axis=1)

def get_vec(word, wordlist, array, lengths):
    ''' Given a certain word we want to find within
    a list of words, corresponding vector array,
    and corresponding vector lengths, returns a
    tuple containing the vector of that word and
    the length of that vector  '''
    word_index = wordlist.index(word)
    word_vector = array[word_index]
    word_length = lengths[word_index]
    return word_vector, word_length

def cosine_similarity(vec1, vec2, lens1, lens2):
    ''' Takes in 2 vectors and their lengths. 
    Returns their cosine similarity. '''
    dot_product = numpy.dot(vec1, vec2)
    return dot_product / (lens1 * lens2)

def score(w1, w2):
    w1_vector, w1_len = get_vec(w1, wordL, array, lengths)
    w2_vector, w2_len = get_vec(w2, wordL, array, lengths)
    return cosine_similarity(w1_vector, w2_vector, w1_len, w2_len)

def test():
    ''' runs the tests cases provided '''
    # test 1
    cat_vector, cat_len = get_vec("cat", wordL, array, lengths)
    dog_vector, dog_len = get_vec("dog", wordL, array, lengths)
    print('Index of cat in list of words:', wordL.index("cat"))
    # test 2
    print("Length of the vector for dog:", dog_len)
    # test 3
    print("Cos similarity between dog and cat vecs:", \
        cosine_similarity(cat_vector, dog_vector, cat_len, dog_len))
    
def main(): 
    f = args.GloVeFILE
    wordL, array = load_text_vectors(f)
    lengths = compute_lengths(array)
    npy = args.npyFILE
    save_glove_vectors(wordL, array, npy)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='utilities.py [-h] GloVeFILE npyFILE')
    parser.add_argument('GloVeFILE', type=argparse.FileType("r"), help='a GloVe text file to read from')
    parser.add_argument('npyFILE', type=argparse.FileType("wb"), help='an .npy file to write the saved numpy data to')
    args = parser.parse_args()
    main()
    
