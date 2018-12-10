import matching_old
import sys
from user_dao_impl import UserDaoImpl
import utilities
import time


class RankingEmployers: #classroom scoring the employers

    def __init__(self, teacher_id, user_dao, utilities):
        self.dao = user_dao
        self.all_employers = self.dao.fetch_all_employers()
        self.employer_ids = list(self.all_employers.keys())
        self.teacher_id = teacher_id
        self.all_teachers = self.dao.fetch_all_teachers()
        self.utilities = utilities
        self.teacher_data = self.all_teachers[teacher_id]

    def getRankedList(self):
        employer_dict = {}
        employer_list = []
        for employer_id in self.employer_ids:
            employer_data = self.all_employers[employer_id]
            match = matching_old.Matching(employer_data, self.teacher_data, self.utilities)
            if not "classes" in match.teacher_data or \
                not "selected_industry_keywords" in match.teacher_data or \
                not "selected_skills_keywords" in match.teacher_data:
                return None # signal that teacher does not have enough data
            if not "selected_industry_keywords" in match.employer_data or \
                not "selected_product_keywords" in match.employer_data or \
                not "selected_service_keywords" in match.employer_data or \
                not "selected_challenge_keywords" in match.employer_data:
                continue    # move onto next employer (this one doesn't have enough info)
            scoreE = match.score_employer()
            employer_dict[employer_id] = scoreE
        for key, value in sorted(employer_dict.items(), key= lambda x: x[1], reverse=True):
             employer_list.append(key)  
             print(str(key) + ": " + str(value))
        return employer_list

def main():
    teacher_id = "49Z7lfsLuihpCaJUZBpuZ0g2rGt1"
    user_dao = UserDaoImpl()
    utils = utilities.Utils()
    rank = RankingEmployers(teacher_id,user_dao, utils)
    print("The list of ranked employers is ", rank.getRankedList())

if __name__ == '__main__':
    main()