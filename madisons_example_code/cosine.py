import argparse
import numpy
from utilities import load_glove_vectors

def cosine_similarity(vec1, vec2, lens1, lens2):
    ''' Takes in 2 vectors and their lengths. 
    Returns their cosine similarity. '''
    dot_product = numpy.dot(vec1, vec2)
    return dot_product / (lens1 * lens2)

def closest_vectors(v, length, words, array, lengths, n=5):
    """six parameters:
    a vector v, that vector’s length length, the list of words words,
    the array array, the list of vector lengths lengths, and an integer n.
    """
    numWords = len(words)
    similarities = numpy.zeros((numWords,), dtype=([('word', "<U30"), ('similarity', numpy.float64)]))
    
    for index in range(0, numWords):
        curWord = words[index]

        curSimilarity = cosine_similarity(v, array[index], length, lengths[index])
        similarities[index] = (words[index], curSimilarity)  
    
    sortedSimilarities = numpy.flip(numpy.sort(similarities, order='similarity'))
    
    return sortedSimilarities[:n]


def main():
    npy = args.npyFILE
    wordL, array, lengths = load_glove_vectors(npy)
    words = ["pink","cat","glove","love","romance","home","flag","cover","commiserate","conceal"]
    for word in words:
        index = wordL.index(word)
        closest = closest_vectors(array[index], lengths[index], wordL, array, lengths)
        print(word)
        print(closest)



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(usage='[-h] [--word WORD] [--file FILE] [--num NUM] npyFILE', description = "Find the n closest words to a given word (if specified) or to all of the words in a text file (if specified). If neither is specified, compute nothing.")
    parser.add_argument('npyFILE', type = argparse.FileType("rb"), help='an .npy file to write the saved numpy data to')
    parser.add_argument('-w', '--word', metavar='WORD', help='a single word')
    parser.add_argument("-f", "--file", metavar='FILE', type = argparse.FileType("r"), help='a text file with one-word-per-line')
    parser.add_argument('-n', '--num', metavar="NUM", help = "find the top n most similar words (default 5)")
    args = parser.parse_args()
    main()

