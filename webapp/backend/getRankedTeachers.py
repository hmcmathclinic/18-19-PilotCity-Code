import matching
import sys
from user_dao_impl import UserDaoImpl

class RankingTeachers: #emplyer scoring the teachers

    def __init__(self, employer_id):
        self.dao = UserDaoImpl()
        self.classroom_ids = self.dao.fetch_all_classrooms()
        self.employer_id = employer_id

    def getRankedList(self):
        classroom_dict = {}
        classroom_list = []
        for classroom in self.classroom_ids:
            match = matching.Matching(self.employer_id, classroom)
            scoreC = match.score_teacher()
            classroom_dict[classroom] = scoreC
        for key, value in sorted(classroom_dict.items(), key= lambda x: x[1], reverse=True):
             classroom_list.append(key)  
             print(str(key) + ": " + str(value))
        return classroom_list

# def main():
    # teacher_id = sys.argv[1]
    # rank = RankingTeachers()
    # print("The list of ranked teachers is ", rank.getRankedList())

# if __name__ == '__main__':
#     # main()