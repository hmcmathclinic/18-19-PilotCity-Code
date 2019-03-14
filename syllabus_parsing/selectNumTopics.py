import utilities
import pickle
from itertools import combinations
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
plt.style.use("ggplot")
matplotlib.rcParams.update({"font.size": 14})

utils = utilities.Utils()

def calculate_coherence(topics_df, top = 3):
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

    nmf_topics_scoreL = []
    nmfTFIDF_topics_scoreL = []
    k_values = range(5, 95, 5)
    for num_topics in k_values:
        topics_fname = "topics/NMF_5_95_5/"+str(num_topics)+"topics_NMFTFIDF_laspositas.sav"
        with open(topics_fname, 'rb') as filehandle:
            topics = pickle.load(filehandle)
        score, skipped_over = calculate_coherence(topics, top=3)
        print(score)
        print(skipped_over)
        nmf_topics_scoreL.append(score)
        topics_fname = "topics/LDA_5_95_5/"+str(num_topics)+"topics_LDATFIDF_laspositas.sav"
        with open(topics_fname, 'rb') as filehandle:
            topics = pickle.load(filehandle)
        score, skipped_over = calculate_coherence(topics, top=3)
        nmfTFIDF_topics_scoreL.append(score)
        print("\n")

    fig = plt.figure(figsize = (35,7))
    # create the line plot
    ax = plt.plot(k_values, nmf_topics_scoreL)
    plt.xticks(k_values)
    plt.xlabel("Number of Topics")
    plt.xlabel("Mean Coherence")
    plt.title("LDA vs. NMF, both with TFIDF")
    # add the points
    plt.scatter(k_values, nmf_topics_scoreL, c="purple", label = "NMF")
    plt.scatter(k_values, nmfTFIDF_topics_scoreL,c="mediumseagreen", label = "LDA")
    # find and annotate the maximum point on the plot
    ymax = max(nmf_topics_scoreL)
    xpos = nmf_topics_scoreL.index(ymax)
    best_kNMF = k_values[xpos]
    plt.annotate("k=%d" % best_kNMF, xy = (best_kNMF, ymax),
                 xytext = (best_kNMF, ymax), 
                 textcoords = "offset points", 
                 fontsize = 16)
    ymax = max(nmfTFIDF_topics_scoreL)
    xpos = nmfTFIDF_topics_scoreL.index(ymax)
    best_knmfTFIDF = k_values[xpos]
    plt.annotate("k=%d" % best_knmfTFIDF, xy = (best_knmfTFIDF, ymax),
                 xytext = (best_knmfTFIDF, ymax), 
                 textcoords = "offset points", 
                 fontsize = 16)
    # show the plot
    plt.show()

main()

