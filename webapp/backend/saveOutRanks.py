import matching
import sys
from user_dao_impl import UserDaoImpl
import utilities
import time
import concurrent.futures
import getRankedClassrooms
import pickle

user_dao = UserDaoImpl()
utils = utilities.Utils()
employer_ids = list(user_dao.fetch_all_employers().keys())

# rankings = {}   # dictionary where keys are employer ids and each  
#                 # value is the ranked classroom list for that employer

indices = {}    # dict where each key is an employer_id and each value is
                # itself a dictionary whose keys are classroom_id's and
                # and each value is the index of that classroom_id in 
                # rankings[employer_id]

for employer_id in employer_ids:
    ranker = getRankedClassrooms.RankingClassrooms(employer_id, user_dao, utils)
    this_employers_ranked_classrooms = ranker.getRankedList()
    this_employers_classroom_indices = {}   # what index does each classroom_id have in 
                                            # this_employers_ranked_classrooms
    if this_employers_ranked_classrooms is None: 
        continue            # skip to next employer if didn't get any classrooms back
    index = 0
    for classroom_id in this_employers_ranked_classrooms:
        this_employers_classroom_indices[classroom_id] = index
        index += 1
    indices[employer_id] = this_employers_classroom_indices # save classroom indices for employer
    print(indices)
    print("\n")

# save out the indices
index_dict = "classroom_indices_all_employers.sav"
with open(index_dict, 'wb') as filehandle:
    pickle.dump(indices, filehandle)
    

