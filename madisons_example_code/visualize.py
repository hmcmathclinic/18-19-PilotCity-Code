import matplotlib
import re
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from utilities import get_vec, load_text_vectors, load_glove_vectors
from sklearn.decomposition import PCA  # put this at the top of your program
import numpy
import argparse

def perform_pca(array, n_components):
    ''' Performs PCA on a given array, allowing
    the user to specify the number of components and
    returns the PCA-transformed array '''
    # For the purposes of this lab, n_components will always be 2.
    pca = PCA(n_components=n_components)
    pc = pca.fit_transform(array)
    return pc

def extract_words(array, wordlist, related_pairs):
    ''' Takes three parameters: the array and wordlist 
    that you read in from the .npy file, along with a 
    list of related pairs. Returns new shorter list of
    words and corresponding numpy array that contains 
    only the vectors for the pairs of words you 
    are extracting.'''
    # create list of lists to later vstack
    new_vecs = []
    new_wordL = []
    for pair in related_pairs:
        if pair[0] in wordlist and pair[1] in wordlist:
            p0_index = wordlist.index(pair[0])
            p1_index = wordlist.index(pair[1])
            new_wordL.extend([pair[0], pair[1]])
            new_vecs.extend([array[p0_index], array[p1_index]])
    new_array = numpy.vstack(new_vecs)
    return new_wordL, new_array

def plot_relations(pca_array, pca_words, figname):
    ''' Takes your pca_array, pca_words, and some 
    name for your figure as parameters and will 
    plot the vectors. '''
    first = range(0, len(pca_words), 2) # even indicies
    second = range(1, len(pca_words), 2)  # odd indicies
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(pca_array[:,0][first], pca_array[:,1][first], c='r', s=50)
    ax.scatter(pca_array[:,0][second], pca_array[:,1][second], c='b', s=50)
    for i in range(len(pca_array)):
        (x,y) = pca_array[i]
        plt.annotate(pca_words[i], xy = (x,y), color = "black")
    for i in range(0, len(pca_array), 2):
        ax.plot(pca_array[:,0][i:i+2], pca_array[:,1][i:i+2],
        linewidth = 1, color = "lightgray")
    plt.savefig(figname)

def read_relations(f):
    ''' reads the relations, and stores them 
    in a list of tuples ''' 
    output = []
    for line in f.readlines():
        list = re.split('\s+', line)
        tuple = (list[0], list[1])
        output.append(tuple)
    return output


def test():
    ''' Checks to see if everything is working properly '''
    
    # Read in the array and words from a saved .npy file 
    # using the load_glove_array function in your utilities.py file
    fp = open("glove.6B.50d.npy", "rb")
    wordL, array, lengths = load_glove_vectors(fp)

    # Read in the list of relations using read_relations
    related_pairs = read_relations(open("data/glove/relations/gender.txt"))
    
    # Extract the vectors you want to plot using extract_words
    related_wordL, related_array = extract_words(array, wordL, related_pairs)

    # Perform PCA on the these vectors using perform_pca
    pca_array = perform_pca(related_array, 2)

    # Plot these vectors using plot_relations
    plot_relations(pca_array, related_wordL, "gender.png")


def main():
    wordL, array, lengths = load_glove_vectors(args.npyFILE)
    related_pairs = read_relations(args.relationsFILE)
    related_wordL, related_array = extract_words(array, wordL, related_pairs)
    pca_array = perform_pca(related_array, 2)
    plot_relations(pca_array, related_wordL, "plots/thatPlotYouJustMade.png")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='visualize.py [-h] npyFILE relationsFILE', 
    description = "Plot the relationship between the GloVe vectors for pairs of related words.")
    parser.add_argument('npyFILE', type=argparse.FileType("rb"), help='an .npy file to read the saved numpy data from')
    parser.add_argument('relationsFILE', type=argparse.FileType("r"), help='a file containing pairs of relations')
    args = parser.parse_args()
    main()