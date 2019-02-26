import matching
import sys
from user_dao_impl import UserDaoImpl
import utilities
import time
import concurrent.futures

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
        future_to_classroom_id = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for classroom in self.classroom_ids:
                classroom_data = self.all_classrooms[classroom]
                if not "teacher_uid" in classroom_data:
                    continue
                teacher_id = classroom_data["teacher_uid"]
                teacher_data = self.all_teachers[teacher_id]
                match = matching.Matching(self.employer_data, teacher_data, classroom_data, self.utilities, self.all_classrooms)
                if not "selected_industry_keywords" in self.employer_data or \
                    not "selected_product_keywords" in self.employer_data or \
                    not "selected_service_keywords" in self.employer_data or \
                    not "selected_challenge_keywords" in self.employer_data:
                    return None # this employer doesn't have enough info to be matched
                if not "classes" in teacher_data or  \
                    not "selected_industry_keywords" in teacher_data or \
                    not "selected_skills_keywords" in teacher_data:
                    continue    # move onto next teacher (this one doesn't have enough info)
                future_to_classroom_id[executor.submit(match.score_classroom)] = classroom

            for future in concurrent.futures.as_completed(future_to_classroom_id):
                classroom = future_to_classroom_id[future]
                try:
                    scoreT = future.result()
                    classroom_dict[classroom] = scoreT
                except Exception as exc:
                    print('%r generated an exception: %s' % (teacher_id, exc))

            for key, _ in sorted(classroom_dict.items(), key= lambda x: x[1], reverse=True):
                classroom_list.append(key)  
            return classroom_list

def main():
    employer_id = "5LSkd65MowXXMzIlyaJRaPgucDE2"
    user_dao = UserDaoImpl()
    utils = utilities.Utils()
    rank = RankingClassrooms(employer_id, user_dao, utils)
    start = time.time()
    ranked_list = rank.getRankedList()
    print(len(ranked_list))
    print("The list of ranked classrooms is ", ranked_list)
    end = time.time()
    print(end - start)
    print("Average time per classroom: {} ".format((end - start)/len(ranked_list)))

if __name__ == '__main__':
    main()
