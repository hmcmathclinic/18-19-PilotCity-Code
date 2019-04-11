# https://arxiv.org/pdf/1701.03227.pdf

import numpy as np
import math
import pickle
from scipy import sparse

# functions used for cleaning, saving, and loading data
def basic_clean(data, remove_set=set()):
	# don’t model spaces or newline characters
	remove_set.add('')
	remove_set.add(' ')
	remove_set.add('\n')
	texts = [[word for word in document.lower().split() if word not in remove_set] for
		document in data]
	return texts

def create_vocabulary(data):
"""
data is a list of documents, where each document is a list of words
returns vocab, a mapping of word to index
"""
	vocab = {}
	counter = 0
	for document in data:
		for word in document:
			if word not in vocab:
				vocab[word] = counter
				counter += 1
	return vocab

def make_repr(data, vocab):
"""
data is a list of documents, where each document is a list of words
vocab is a dictionary mapping each vocabulary word to an integer
returns output_matrix that is nDocuments by nVocab, where M_ij represents
the number of times word j appears in document i
"""
	output_matrix = np.zeros((len(data), len(vocab)))
	for doc_index, document in enumerate(data):
		for word in document:
			output_matrix[doc_index][vocab[word]] += 1
	return output_matrix

def save_data(output_matrix, output_path):
"""
data is saved in scipy sparse matrix format as a pickle file
"""
	sparse_m = sparse.csr_matrix(m)
	with open(output_path + ".pkl", "w") as f:
		pickle.dump(sparse_m, f)

	# functions used to generate informative priors

	text = ["Alice was beginning to get very tired of sitting", \
			"by her sister on the bank ,", \
			"and of having nothing to do :", \
			"once or twice she had peeped into the book her sister was reading", \
			"but it had no pictures or conversations in it", \
			"’ and what is the use of a book , ’", \
			"thought Alice", \
			"’ without pictures or conversations ? ’"]
	keywords = [’book’, ’pictures’, ’conversations’]
	vocab = sorted(list(set(" ".join(text).split())))

def prior_data(data, keywords):
	data_dict = {}
	num_documents = float(len(data))
	num_words = 0
	for index, words in enumerate(data):
		words = words.split(" ")
		doc_length = float(len(words))
		num_words += doc_length
	for word in set(words):
		word_count = sum([word == i for i in words])
		if word not in data_dict:
			data_dict[word] = {"wordCount": 0, "tf": {}, "keyword": 0,
				"numDocAppearance": 0}
		data_dict[word]["wordCount"] += word_count
		data_dict[word]["tf"][index] = word_count / doc_length
		data_dict[word]["numDocAppearance"] += 1

	for word in keywords:
		data_dict[word]["keyword"] = 1

	for key in data_dict:
		data_dict[key]["wf"] = data_dict[key]["wordCount"] / num_words
		data_dict[key]["idf"] = math.log(num_documents /
			data_dict[key]["numDocAppearance"])
		data_dict[key]["tfidf"] = np.mean(data_dict[key]["tf"].values()) *
			data_dict[key]["idf"]

	return data_dict

def build_prior(prior_data, vocab, num_stopword_topics=0, num_wf_topics=0, 
	num_tf_topics=10, num_keyword_topics=0, c1=1, c2=10):

	def build_stopword_topic():
		return [1.0 for _ in vocab]

	def build_wf_topic():
		return [1.0 / prior_data[word]["wf"] for word in vocab]

	def build_tfidf_topic():
		return [c1 * prior_data[word]["tfidf"] for word in vocab]

	def build_keyword_topic():
		return [c2 * prior_data[word]["keyword"] for word in vocab]
	prior = [build_stopword_topic() for i in range(num_stopword_topics)] + \
			[build_wf_topic() for i in range(num_wf_topics)] + \
			[build_tfidf_topic() for i in range(num_tf_topics)] + \
			[build_keyword_topic() for i in range(num_keyword_topics)]
	return prior


# example usage:
prior_statistics = prior_data(text, keywords)
model_prior = build_prior("wf", prior_statistics, vocab, 1, 1, 1, 1)
