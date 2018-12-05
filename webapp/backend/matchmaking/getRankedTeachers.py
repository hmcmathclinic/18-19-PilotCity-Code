import matching
import sys
from user_dao_impl import UserDaoImpl

class RankingTeachers: #employer scoring the teachers

    def __init__(self, employer_id):
        self.dao = UserDaoImpl()
        self.employer_id = employer_id
        self.teacher_ids = self.dao.fetch_all_teachers()

    def getRankedList(self):
        teacher_dict = {}
        teacher_list = []
        for teacher in self.teacher_ids:
            match = matching.Matching(self.employer_id, teacher)
            scoreT = match.score_teacher()
            teacher_dict[teacher] = scoreT
        for key, value in sorted(teacher_dict, key= teacher_dict.get(), reverse=False):
            teacher_list = teacher_list.append(key)  
        return teacher_list

def main():
    employer_id = sys.argv[1]
    rank = RankingTeachers(employer_id)
    print("The list of ranked teachers is ", rank.getRankedList())

if __name__ == '__main__':
    main()