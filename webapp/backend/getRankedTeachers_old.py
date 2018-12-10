import matching_old
import sys
from user_dao_impl import UserDaoImpl
import time
import utilities


class RankingTeachers: #emplyer scoring the teachers


    def __init__(self, employer_id, user_dao, utilities):
        self.dao = user_dao
        self.all_teachers = self.dao.fetch_all_teachers()
        self.teacher_ids = list(self.all_teachers.keys())
        self.employer_data = self.dao.fetch_employer_data(employer_id)
        self.utilities = utilities
        self.employer_id = employer_id


    def getRankedList(self):
        teacher_dict = {}
        teacher_list = []
        for teacher in self.teacher_ids:
            teacher_data = self.all_teachers[teacher]
            match = matching_old.Matching(self.employer_data, teacher_data, self.utilities)
            if not "selected_industry_keywords" in match.employer_data or \
                not "selected_product_keywords" in match.employer_data or \
                not "selected_service_keywords" in match.employer_data or \
                not "selected_challenge_keywords" in match.employer_data:
                return None # this employer doesn't have enough info to be matched
            if not "classes" in match.teacher_data or  \
                not "selected_industry_keywords" in match.teacher_data or \
                not "selected_skills_keywords" in match.teacher_data:
                continue    # move onto next teacher (this one doesn't have enough info)
            scoreT = match.score_teacher()
            teacher_dict[teacher] = scoreT
        for key, value in sorted(teacher_dict.items(), key= lambda x: x[1], reverse=True):
            teacher_list.append(key)  
            print(str(key) + ": " + str(value))
        return teacher_list


def main():
    employer_id = "7bNr6B30iscz7hL4zAvSqiN1g0l2"
    user_dao = UserDaoImpl()
    utils = utilities.Utils()
    rank = RankingTeachers(employer_id, user_dao, utils)
    print("The list of ranked teachers is ", rank.getRankedList())

if __name__ == '__main__':
    main()