import matching
from user_dao_impl import UserDaoImpl

class RankingEmployers: #teacher scoring the employers

    def __init__(self, teacher_id):
        self.employer_ids = []
        self.teacher_id = teacher_id

    def getRankedList():
        employer_dict = {}
        employer_list = []
        for employer in self.employer_ids:
            match = Matching(teacher_id, employer)
            scoreE = match.score_employer()
            employer_dict[employer] = scoreE
        for key, value in sorted(employer_dict.iteritems(), key=lambda (k,v): (v,k)):
            employer_list = employer_list.append(key)  
        return employer_list

def main():
    teacher_id = sys.argv[1:][1]
    rank = RankingTeachers(teacher_id)
    print("The list of ranked employers is ", rank.getRankedList())

if __name__ == '__main__':
    main()