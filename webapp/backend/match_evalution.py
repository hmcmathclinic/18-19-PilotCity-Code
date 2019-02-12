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
        scoreL = [self.getIndexFromRank(classroom_id) for classroom_id in self.myClassrooms]
        print(scoreL)
        idealRank = (len(scoreL) - 1)*len(scoreL)/2
        return sum(scoreL)/float(len(scoreL)) - idealRank
        
    def getIndexFromRank(self, classroom_id):
        ''' Return the index of classroom_id in self.rankings '''
        print(self.rankingIDs)
        for index in range(len(self.rankings)):
            if self.rankings[index] == classroom_id:
                return index

def main():
    employer_id = "OMVVQHvDRyMdF4wRQe22gllXgcn1"
    user_dao = UserDaoImpl()
    utils = utilities.Utils()
    eval = EvalThisEmployer(employer_id, user_dao, utils)
    print(eval.scoreAllClassrooms())

if __name__ == "__main__":
    main()