import matching
import sys
from user_dao_impl import UserDaoImpl

class RankingEmployers: #classroom scoring the employers

    def __init__(self, classroom_id):
        self.dao = UserDaoImpl()
        self.employer_ids = self.dao.fetch_all_employers()
        self.classroom_id = classroom_id

    def getRankedList(self):
        employer_dict = {}
        employer_list = []
        for employer in self.employer_ids:
            match = matching.Matching(employer, self.teacher_id)
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
            employer_dict[employer] = scoreE
        for key, value in sorted(employer_dict.items(), key= lambda x: x[1], reverse=True):
             employer_list.append(key)  
             print(str(key) + ": " + str(value))
        return employer_list

def main():
    teacher_id = sys.argv[1]
    rank = RankingEmployers(teacher_id)
    print("The list of ranked employers is ", rank.getRankedList())

if __name__ == '__main__':
    main()