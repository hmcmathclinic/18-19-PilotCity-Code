import matching
import sys
from user_dao_impl import UserDaoImpl

class RankingTeachers: #emplyer scoring the teachers

    def __init__(self):
        self.dao = UserDaoImpl()
        self.teacher_ids = self.dao.fetch_all_teachers()
        self.employer_id = self.dao.fetch_all_employers()[0]

    def getRankedList(self):
        teacher_dict = {}
        teacher_list = []
        for teacher in self.teacher_ids:
            match = matching.Matching(self.employer_id, teacher)
            scoreT = match.score_teacher()
            teacher_dict[teacher] = scoreT
        for key, value in sorted(teacher_dict.items(), key= lambda x: x[1], reverse=True):
             teacher_list.append(key)  
             print(str(key) + ": " + str(value))
        return teacher_list

def main():
    # teacher_id = sys.argv[1]
    rank = RankingTeachers()
    print("The list of ranked teachers is ", rank.getRankedList())

if __name__ == '__main__':
    main()