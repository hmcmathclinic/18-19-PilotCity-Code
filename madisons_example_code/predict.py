from utilities import load_glove_vectors, compute_lengths
from cosine import closest_vectors
from visualize import extract_words, read_relations
import argparse
import random
import numpy

def average_difference(orig_array, word_list, relations_list):
    ''' Returns average difference between the vectors of two
    words in a pair over all pairs in a relation'''
    related_wordL, related_array = extract_words(orig_array, word_list, relations_list)
    avg_list = []
    for index in range(0, len(related_wordL), 2):
        index2 = index + 1
        avg_list.append(related_array[index] - related_array[index2])

    vec_average = sum(avg_list) / len(avg_list)
    return vec_average

def main():
    #gather total word list and array from npy file
    wordL, array, lengths = load_glove_vectors(args.npyFILE)
    #get related pairs list
    related_pairs = read_relations(args.relationsFILE)
    #shuffle the list for randomness
    random.shuffle(related_pairs)
    #create training pairs list
    training_relations = related_pairs[:int(len(related_pairs)*.8)]
    #create test pairs list
    test_relations = related_pairs[int(len(related_pairs)*.8):]
    #calculate average difference for the pairs as a whole
    avg_difference = average_difference(array, wordL, training_relations)
    #get related word list and array
    related_wordL, related_array = extract_words(array, wordL, related_pairs)
    #leghts of full related_array
    test_lengths = compute_lengths(related_array)
    #counters for place of first word in similar words
    is_most_similar = 0
    is_top_10 = 0
    similarity_index = 0

    is_most_similar_2 = 0
    is_top_10_2 = 0
    similarity_index_2 = 0

    num_invalid = 0
    for relation in test_relations:
        first, second = relation
        if not ((first in related_wordL) and (second in related_wordL)):
            num_invalid += 1
            continue
        index = related_wordL.index(second)
        #vector of second word in pair
        vec = related_array[index]
        #list of 99 closest words to second
        closest = closest_vectors(vec, test_lengths[index], wordL, array, lengths, 100)[1:]
        top_closest = closest[:10]
        if closest[0][0] == first:
            is_most_similar += 1
        contained = [item for item in top_closest if item[0] == first]
        if len(contained) > 0:
            is_top_10 += 1
        contained = [item for item in closest if item[0] == first]
        if len(contained) > 0:
            similarity_index += numpy.where(closest == contained[0])[0][0] #closest.index(contained[0])
        else:
            similarity_index += 100
        
        new_avg_vec = vec + avg_difference
        new_len = numpy.linalg.norm(new_avg_vec)

        closest = closest_vectors(new_avg_vec, new_len, wordL, array, lengths, 100)
        top_closest = closest[:10]
        if closest[0][0] == first:
            is_most_similar_2 += 1
        contained = [item for item in top_closest if item[0] == first]
        if len(contained) > 0:
            is_top_10_2 += 1
        contained = [item for item in closest if item[0] == first]
        if len(contained) > 0:
            similarity_index_2 += numpy.where(closest == contained[0])[0][0]
        else:
            similarity_index_2 += 100

    num_valid_pairs = len(test_relations) - num_invalid
    print("FOR JUST PLAIN WORDS")
    print("average that the first word was the most similar to the second:")
    print(is_most_similar / num_valid_pairs)
    print("average that the first word was in the top 10 most similar to the second:")
    print(is_top_10 / num_valid_pairs)
    print("average index of first word:")
    print(similarity_index / num_valid_pairs)

    print("FOR WORD VECTOR PLUS AVERAGE DIFFERENCE VECTOR")
    print("average that the first word was the most similar to the second:")
    print(is_most_similar_2 / num_valid_pairs)
    print("average that the first word was in the top 10 most similar to the second:")
    print(is_top_10_2 / num_valid_pairs)
    print("average index of first word:")
    print(similarity_index_2 / num_valid_pairs)
    
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='predict.py [-h] npyFILE relationsFILE', 
    description = "Find the vector that connects the first word to the second word in each relations pair, and then take the average of these to find the average connecting vector for the set.")
    parser.add_argument('npyFILE', type=argparse.FileType("rb"), help='an .npy file to read the saved numpy data from')
    parser.add_argument('relationsFILE', type=argparse.FileType("r"), help='a file containing pairs of relations')
    args = parser.parse_args()
    main()
