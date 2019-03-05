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

# Load-in results for all employers from match-making 
# algorithm. Index dict is a  dict where each key is an 
# employer_id and each value is itself a dictionary whose 
# keys are classroom_id's and and each value is the index 
# of that classroom_id in the rankings for this employer_id 
# as output by our Alg

index_dict = "classroom_indices_all_employers.sav"
with open(index_dict, 'rb') as filehandle:
    indices = pickle.load(filehandle)

employer_ranks = {} # keys are employer_ids, values are list 
                    # of where their assigned classrooms fell 
                    # in our alg's ranking

for employer_id in employer_ids:
    thisEmployersData = user_dao.fetch_employer_data(employer_id)
    if employer_id in indices and \
        'challenge_uids' in thisEmployersData and \
        thisEmployersData['challenge_uids'] != [] :
        ranksOfThisEmployersClassrooms = []
        thisEmployersIndices = indices[employer_id]
        for challenge_id in thisEmployersData['challenge_uids']: #dicts
            challenge_info = user_dao.fetch_challenge_data(challenge_id)
            if (not(challenge_info is None) and 'classroom' in challenge_info \
                and challenge_info['classroom'] != []):
                classroom_id = challenge_info['classroom'][0]
                print(thisEmployersIndices)
                print(classroom_id)
                classrooms_index_in_rank = thisEmployersIndices[classroom_id]
                ranksOfThisEmployersClassrooms.append(classrooms_index_in_rank)
        # at the end, store ranks for this employer's assigned classrooms
        employer_ranks[employer_id] = ranksOfThisEmployersClassrooms

print(employer_ranks)

# save out the ranks for each employer's assigned classrooms
ranks_file= "assigned_classroom_ranks_all_employers.sav"
with open(ranks_file, 'wb') as filehandle:
    pickle.dump(employer_ranks, filehandle)