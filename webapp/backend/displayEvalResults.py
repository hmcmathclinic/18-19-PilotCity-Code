import pickle
from statistics import median

ranks_file= "assigned_classroom_ranks_all_employers.sav"
with open(ranks_file, 'rb') as filehandle:
    employer_ranks = pickle.load(filehandle)

for employer_id, ranks in employer_ranks.items():
    print(employer_id)
    print(ranks)
    print(len(ranks))
    ideal = sum(range(0,len(ranks)))/float((len(ranks)))
    score_by_median = median(ranks) - ideal
    print("score_by_median:", score_by_median)
    score_by_mean = sum(ranks)/float(len(ranks)) - ideal
    print("score_by_mean:", score_by_mean)
    print("\n")