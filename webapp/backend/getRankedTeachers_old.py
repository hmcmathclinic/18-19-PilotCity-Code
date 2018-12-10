import matching_old
import sys
from user_dao_impl import UserDaoImpl
import time


class RankingTeachers: #emplyer scoring the teachers

    def __init__(self, employer_id):
        self.dao = UserDaoImpl()
        start = time.time()
        self.teacher_ids = self.dao.fetch_all_teachers()
        end = time.time()
        print("init time - {}".format(end - start))
        self.employer_id = employer_id

    def getRankedList(self):
        teacher_dict = {}
        teacher_list = []
        total_time = 0
        for teacher in self.teacher_ids:
            start = time.time()
            match = matching_old.Matching(self.employer_id, teacher)
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
            end = time.time()
            total_time += end - start
            print("time per teacher comp - {}".format(end - start))
        for key, value in sorted(teacher_dict.items(), key= lambda x: x[1], reverse=True):
            teacher_list.append(key)  
            print(str(key) + ": " + str(value))
        print("Total Time : {}".format(total_time))
        return teacher_list

def main():
    employer_id = "7bNr6B30iscz7hL4zAvSqiN1g0l2"

    rank = RankingTeachers(employer_id)
    print("The list of ranked teachers is ", rank.getRankedList())

if __name__ == '__main__':
    main()