import matching
import sys
from user_dao_impl import UserDaoImpl

class RankingClassrooms: #emplyer scoring the classrooms

    def __init__(self):
        self.dao = UserDaoImpl()
        self.classroom_ids = self.dao.fetch_all_classrooms()
        self.employer_id = self.dao.fetch_all_employers()[0]

    def getRankedList(self):
        classroom_dict = {}
        classroom_list = []
        for classroom in self.classroom_ids:
            match = matching.Matching(self.employer_id, classroom)
            if not "selected_industry_keywords" in match.employer_data or \
                not "selected_product_keywords" in match.employer_data or \
                not "selected_service_keywords" in match.employer_data or \
                not "selected_challenge_keywords" in match.employer_data:
                return None # this employer doesn't have enough info to be matched
            if not "classes" in match.teacher_data or  \
                not "selected_industry_keywords" in match.teacher_data or \
                not "selected_skills_keywords" in match.teacher_data:
                continue    # move onto next teacher (this one doesn't have enough info)
            scoreC = match.score_classroom()
            classroom_dict[classroom] = scoreC
        for key, value in sorted(classroom_dict.items(), key= lambda x: x[1], reverse=True):
             classroom_list.append(key)  
             print(str(key) + ": " + str(value))
        return classroom_list

def main():
    rank = RankingClassrooms()
    print("The list of ranked classrooms is ", rank.getRankedList())

if __name__ == '__main__':
    main()