import matching
import sys
from user_dao_impl import UserDaoImpl
import utilities
import time
import concurrent.futures

class RankingEmployers: #classroom scoring the employers

    def __init__(self, classroom_id, user_dao, utilities):
        self.dao = user_dao
        self.classroom_id = classroom_id
        self.classroom_data = self.dao.fetch_classroom_data(self.classroom_id)
        self.all_employers = self.dao.fetch_all_employers() # used to be employer_ids
        self.employer_ids = list(self.all_employers.keys())
        self.teacher_id = self.classroom_data["teacher_uid"]
        self.utilities = utilities
        self.teacher_data = self.dao.fetch_teacher_data(self.teacher_id)

    def getRankedList(self):
        employer_dict = {}
        employer_list = []
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        future_to_employer_id = {}
        for employer_id in self.employer_ids:
            employer_data = self.all_employers[employer_id]
            match = matching.Matching(employer_data, self.teacher_data, self.classroom_data, self.utilities)
            if not "classes" in match.teacher_data or \
                not "selected_industry_keywords" in match.teacher_data or \
                not "selected_skills_keywords" in match.teacher_data:
                return None # signal that teacher does not have enough data
            if not "selected_industry_keywords" in match.employer_data or \
                not "selected_product_keywords" in match.employer_data or \
                not "selected_service_keywords" in match.employer_data or \
                not "selected_challenge_keywords" in match.employer_data:
                continue    # move onto next employer (this one doesn't have enough info)
            future_to_employer_id[executor.submit(match.score_employer)] = employer_id
            #scoreE = match.score_employer()
            #employer_dict[employer_id] = scoreE
        for future in concurrent.futures.as_completed(future_to_employer_id):
            employer_id = future_to_employer_id[future]
            try:
                scoreE = future.result()
                employer_dict[employer_id] = scoreE
            except Exception as exc:
                print('%r generated an exception: %s' % (employer_id, exc))
        for key, value in sorted(employer_dict.items(), key= lambda x: x[1], reverse=True):
            employer_list.append(key)  
            print(str(key) + ": " + str(value))
        return employer_list

def main():
    classroom_id = "49Z7lfsLuihpCaJUZBpuZ0g2rGt10"
    user_dao = UserDaoImpl()
    utils = utilities.Utils()
    rank = RankingEmployers(classroom_id,user_dao, utils)
    start = time.time()
    ranked_list = rank.getRankedList()
    print(len(ranked_list))
    print("The list of ranked employers is ", ranked_list)
    end = time.time()
    print("Runtime for getting ranked list: {} ".format(end - start))
    print("Average time per classroom: {} ".format((end - start)/len(ranked_list)))

if __name__ == '__main__':
    main()