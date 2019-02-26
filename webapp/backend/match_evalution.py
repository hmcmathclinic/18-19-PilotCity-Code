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

        self.myChallengeIDs = self.employer_data['challenge_uids'] # ids
        self.myChallenges = [self.dao.fetch_challenge_data(id) for id in self.myChallengeIDs] # dicts

        self.myClassrooms = [challenge['classroom'] for challenge in self.myChallenges \
            if not(challenge is None) and ('classroom' in challenge and challenge['classroom'] != [])]

        self.ranker = getRankedClassrooms.RankingClassrooms(employer_id, user_dao, utilities)
        
        self.rankingIDs = self.ranker.getRankedList()  # ids
        self.rankings = [self.dao.fetch_classroom_data(id) for id in self.rankingIDs] # dicts

        # self.myInvitedClassrooms = self.employer_data['invited'] # classroom ids
        # self.classroomsWhoRequestedMe = self.employer_data['request']
        
    def scoreAllClassrooms(self):
        ''' Returns the average normalized rank of the indices of 
        self.myClassrooms in self.rankings '''
        for id in self.myClassrooms:
            print(id)
            print(id[0])
        scoreL = [self.getIndexFromRank(classroom_id[0]) for classroom_id in self.myClassrooms]
        print(scoreL)
        # note:
        # kV0g3Wo35iW489WXL4ooXTzHFxk2
        # [29, 35, 30, 31, 32, 20, 21, 76, 29, 29]
        # my score =  28.700000000000003
        # kllt9h5NFJhwgEybOyhfcnREQ9c2
        # [15, 10, 21, 4, 0, 3, 1, 2, 117, 119, 118, 67, 56, 52, 54]
        # my score =  35.6
        idealRank = sum(range(0,len(scoreL)))/float((len(scoreL))) # average of ideal rank
        return sum(scoreL)/float(len(scoreL)) - idealRank # the higher this non-zero number, the better
        
    def getIndexFromRank(self, classroom_id):
        ''' Return the index of classroom_id in self.rankings '''
        for index in range(len(self.rankings)):
            if self.rankingIDs[index] == classroom_id:
                return index

    # def scoreInvitesAndRequests(self):
    #     ''' Compare Matchmaking Output with "otherPossibilities" (this employer's invited 
    #     classrooms and the classrooms who requested this employer) '''
    #     otherPossibilities = self.employer_data['invited'] + self.employer_data['requests']
    #     for classroom_id in otherPossibilities


class evalAllEmployers:

    def __init__(self, user_dao, utilities):
        self.dao = user_dao
        self.utilities = utilities
        self.employer_ids = list(self.dao.fetch_all_employers().keys())
        for id in self.employer_ids:
            print(id)
            thisEmployersData = self.dao.fetch_employer_data(id)
            if 'challenge_uids' in thisEmployersData and \
                thisEmployersData['challenge_uids'] != [] :
                thisEmployersChallenges = [self.dao.fetch_challenge_data(id) for id in thisEmployersData['challenge_uids']] # dicts 
                thisEmployersClassrooms = []
                for challenge in thisEmployersChallenges:
                    if (not(challenge is None) and 'classroom' in challenge and challenge['classroom'] != []):
                        thisEmployersClassrooms.append(challenge['classroom'])
                        print("\n")
                # thisEmployersClassrooms = [challenge['classroom'] for challenge in thisEmployersChallenges \
                #     if ('classroom' in challenge and challenge['classroom'] != [])]
            if 'challenge_uids' in thisEmployersData and \
                thisEmployersData['challenge_uids'] != [] and \
                thisEmployersClassrooms != [] and \
                id != '5LSkd65MowXXMzIlyaJRaPgucDE2': # this is PilotCity!
                print(id)
                thisEval = EvalThisEmployer(id, self.dao, self.utilities)
                print("my score = ", thisEval.scoreAllClassrooms())
        # self.evalObjects = [EvalThisEmployer(id, self.dao, self.utilities) 
        #                     for id in self.employer_ids 
        #                     if 'challenge_uids' in self.dao.fetch_employer_data(id)]

    def getOverallScore(self):
        ''' Returns average score across all employers'''
        scores = []
        for evalObject in self.evalObjects:
            scores.append(evalObject.scoreAllClassrooms())
        return sum(scores)/float(len(scores))

def main():
    employer_id = "dCKmzXDjB0ZEAlYN7cT9kRBPu6E3"
    user_dao = UserDaoImpl()
    utils = utilities.Utils()
    evalAll = evalAllEmployers(user_dao, utils)
    print("Overall score is ", evalAll.getOverallScore())
    print(evalAll.employer_ids)
    print("\n")
    print(evalAll.evalObjects)
    # eval = EvalThisEmployer(employer_id, user_dao, utils)
    # print(eval.scoreAllClassrooms())

if __name__ == "__main__":
    main()