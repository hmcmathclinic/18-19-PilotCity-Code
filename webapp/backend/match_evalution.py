import matching
import sys
from user_dao_impl import UserDaoImpl
import utilities
import time
import concurrent.futures
import getRankedClassrooms 

class EvalThisEmployer:

    ''' Evaluates this Employer versus our matches '''
    
    def __init__(self, employer_id, user_dao, utilities):

        self.dao = user_dao
        self.employer_data = self.dao.fetch_employer_data(employer_id)
        self.utilities = utilities
        self.ranker = getRankedClassrooms.RankingClassrooms(employer_id, user_dao, utilities)
        
        self.rankingIDs = self.ranker.getRankedList()  # ids
        self.rankings = [self.dao.fetch_classroom_data(id) for id in self.rankingIDs] # dicts

        self.myChallengeIDs = self.employer_data['challenge_uids'] # ids
        self.myChallenges = [self.dao.fetch_challenge_data(id) for id in self.myChallengeIDs] # dicts
        
        self.myClassrooms = [challenge['classroom'] for challenge in self.myChallenges]
        
    def scoreAllClassrooms(self):
        ''' Returns the average normalized rank of the indices of 
        self.myClassrooms in self.rankings '''
        scoreL = [self.getIndexFromRank(classroom_id[0]) for classroom_id in self.myClassrooms]
        idealRank = ((len(scoreL) - 1)*len(scoreL)/2)/2
        return sum(scoreL)/float(len(scoreL)) - idealRank
        
    def getIndexFromRank(self, classroom_id):
        ''' Return the index of classroom_id in self.rankings '''
        for index in range(len(self.rankings)):
            if self.rankingIDs[index] == classroom_id:
                return index

    def scoreInvite(self):


class evalAllEmployers:

    def __init__(self, user_dao, utilities):
        self.dao = user_dao
        self.utilities = utilities
        self.employer_ids = list(self.dao.fetch_all_employers().keys())
        self.evalObjects = [EvalThisEmployer(id, self.dao, self.utilities) 
                            for id in self.employer_ids]

    def getOverallScore(self):
        ''' Returns average score across all employers'''
        scores = []
        for evalObject in self.evalObjects:
            scores.append(evalObject.scoreAllClassrooms())
        return sum(scores)/float(len(scores))

def main():
    employer_id = "OMVVQHvDRyMdF4wRQe22gllXgcn1"
    user_dao = UserDaoImpl()
    utils = utilities.Utils()
    evalAll = evalAllEmployers(user_dao, utils)
    print(evalAll.employer_ids)
    print("\n")
    print(evalAll.evalObjects)
    eval = EvalThisEmployer(employer_id, user_dao, utils)
    print(eval.scoreAllClassrooms())

if __name__ == "__main__":
    main()