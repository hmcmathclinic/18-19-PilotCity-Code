import matching
import sys
from user_dao_impl import UserDaoImpl
import utilities

class RankingClassrooms: #emplyer scoring the classrooms

    def __init__(self, employer_id, user_dao, utilities):
        self.dao = user_dao
        self.all_classrooms = self.dao.fetch_all_classrooms() 
        self.all_teachers = self.dao.fetch_all_teachers()
        self.classroom_ids = list(self.all_classrooms.keys())
        self.employer_data = self.dao.fetch_employer_data(employer_id)
        self.utilities = utilities
        self.employer_id = employer_id

    def getRankedList(self):
        classroom_dict = {}
        classroom_list = []
        for classroom in self.classroom_ids:
            classroom_data = self.all_classrooms[classroom]
            teacher_id = classroom_data["teacher_uid"]
            teacher_data = self.all_teachers[teacher_id]
            match = matching.Matching(self.employer_data, teacher_data, classroom_data, self.utilities)
            if not "selected_industry_keywords" in self.employer_data or \
                not "selected_product_keywords" in self.employer_data or \
                not "selected_service_keywords" in self.employer_data or \
                not "selected_challenge_keywords" in self.employer_data:
                return None # this employer doesn't have enough info to be matched
            if not "classes" in teacher_data or  \
                not "selected_industry_keywords" in teacher_data or \
                not "selected_skills_keywords" in teacher_data:
                continue    # move onto next teacher (this one doesn't have enough info)
            scoreC = match.score_classroom()
            classroom_dict[classroom] = scoreC
        for key, value in sorted(classroom_dict.items(), key= lambda x: x[1], reverse=True):
             classroom_list.append(key)  
             print(str(key) + ": " + str(value))
        return classroom_list

def main():
    employer_id = "7bNr6B30iscz7hL4zAvSqiN1g0l2"
    user_dao = UserDaoImpl()
    utils = utilities.Utils()
    rank = RankingTeachers(employer_id, user_dao, utils)
    print("The list of ranked classrooms is ", rank.getRankedList())

if __name__ == '__main__':
    main()