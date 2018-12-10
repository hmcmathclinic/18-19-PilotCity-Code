import matching
import sys
from user_dao_impl import UserDaoImpl

class RankingTeachers: #emplyer scoring the teachers

    def __init__(self, employer_id):
        self.dao = UserDaoImpl()
        self.classroom_ids = self.dao.fetch_all_classrooms()
        self.employer_id = employer_id

    def getRankedList(self):
        teacher_dict = {}
        teacher_list = []
        for teacher in self.teacher_ids:
            match = matching.Matching(self.employer_id, teacher)
            if not "selected_industry_keywords" in match.employer_data or \
                not "selected_product_keywords" in match.employer_data or \
                not "selected_service_keywords" in match.employer_data or \
                not "selected_challenge_keywords" in match.employer_data:
                return None # this employer doesn't have enough info to be matched
            if not "classes" in match.teacher_data or \ 
                not "selected_industry_keywords" in match.teacher_data or \
                not "selected_skills_keywords" in match.teacher_data:
                continue    # move onto next teacher (this one doesn't have enough info)
            scoreT = match.score_teacher()
            teacher_dict[teacher] = scoreT
        for key, value in sorted(teacher_dict.items(), key= lambda x: x[1], reverse=True):
            teacher_list.append(key)  
            print(str(key) + ": " + str(value))
        return classroom_list

# def main():
    # teacher_id = sys.argv[1]
    # rank = RankingTeachers()
    # print("The list of ranked teachers is ", rank.getRankedList())

# if __name__ == '__main__':
#     # main()