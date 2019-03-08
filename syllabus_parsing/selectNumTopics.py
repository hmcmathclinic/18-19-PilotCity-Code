import utilities
import pickle
from itertools import combinations
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
plt.style.use("ggplot")
matplotlib.rcParams.update({"font.size": 14})

utils = utilities.Utils()

def calculate_coherence(topics_df, top = 5):
    skipped_over = 0
    num_topics = topics_df.shape[1]
    print(num_topics)
    topics_df = topics_df.head(top) # how many words do we actually want to look at?
    overall_coherence = 0.0
    for column in topics_df:
        # check each pair of terms
        pair_scores = []
        for pair in combinations(topics_df[column], 2 ):
            if not pair[0] in utils.wordL or not pair[1] in utils.wordL:
                skipped_over += 1
                continue   # skip if not there 
            score = utils.score(pair[0], pair[1]) 
            pair_scores.append(score)
            if score > 1 or score < -1: 
                print("problem!")
                print(score)
        # get the mean for all pairs in this topic
        topic_score = sum(pair_scores) / len(pair_scores)
        overall_coherence += topic_score
    # get the mean score across all topics
    return overall_coherence / num_topics, skipped_over

def main():
    utils = utilities.Utils()
    #utils.score(w1.lower(), w2.lower())

    topics_fname = "topics/20topics_nmf_laspositas.sav"
    with open(topics_fname, 'rb') as filehandle:
        topics20_df = pickle.load(filehandle)

    topics_fname = "topics/50topics_nmf_laspositas.sav"
    with open(topics_fname, 'rb') as filehandle:
        topics50_df = pickle.load(filehandle)

    topics_fname = "topics/100topics_nmf_laspositas.sav"
    with open(topics_fname, 'rb') as filehandle:
        topics100_df = pickle.load(filehandle)

    topics_fname = "topics/200topics_nmf_laspositas.sav"
    with open(topics_fname, 'rb') as filehandle:
        topics200_df = pickle.load(filehandle)

    topic_options = [topics20_df, topics50_df, topics100_df, topics200_df]

    scores = []
    skipped = []
    for topics in topic_options:
        score, skipped_over = calculate_coherence(topics, top=5)
        scores.append(score)
        skipped.append(skipped_over)
    print(scores)
    print(skipped)



