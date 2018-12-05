import matching
import sys
from user_dao_impl import UserDaoImpl

class RankingEmployers: #teacher scoring the employers

    def __init__(self, teacher_id):
        self.dao = UserDaoImpl()
        self.employer_ids = self.dao.fetch_all_employers()
        self.teacher_id = teacher_id

    def getRankedList(self):
        employer_dict = {}
        employer_list = []
        for employer in self.employer_ids:
            match = matching.Matching(employer, self.teacher_id)
            scoreE = match.score_employer()
            employer_dict[employer] = scoreE
        for key, value in sorted(employer_dict.items(), key= lambda x: x[1], reverse=True):
             employer_list.append(key)  
             print(str(key) + ": " + str(value))
        return employer_list

# def main():
#     # teacher_id = sys.argv[1]
#     # rank = RankingEmployers()
#     print("The list of ranked employers is ", rank.getRankedList())

# if __name__ == '__main__':
    # main()