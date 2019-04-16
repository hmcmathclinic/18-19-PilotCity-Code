import concurrent
from user_dao_impl import UserDaoImpl
import utilities
import getRankedEmployers
import getRankedClassrooms

user_dao = UserDaoImpl()

def compute_and_push_ranking(id_, is_classroom):
    dao = UserDaoImpl()
    utils_ = utilities.Utils()
    if is_classroom:
        ranker = getRankedEmployers.RankingEmployers(id_, dao, utils_)
    else:
        ranker = getRankedClassrooms.RankingClassrooms(id_, dao, utils_)
    ranked_list = ranker.getRankedList()
    if not ranked_list:
        ranked_list = []
    try:
        dao.push_ranking(id_, {"rankings":ranked_list})
        return 0
    except Exception as exc:
        print('%r generated an exception: %s' % (id_, exc))
        return 1



def update_ranking():
    all_classrooms = user_dao.fetch_all_classrooms()
    all_employers = user_dao.fetch_all_employers()
    employers_ids = list(all_employers.keys())
    classroom_ids = list(all_classrooms.keys())
    future_to_id = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for classroom_id in classroom_ids:
            future_to_id[executor.submit(compute_and_push_ranking, classroom_id, True)] = classroom_id

        for employer_id in employers_ids:
            future_to_id[executor.submit(compute_and_push_ranking, employer_id, False)] = employer_id

        for future in concurrent.futures.as_completed(future_to_id):
            id_ = future_to_id[future]
            try:
                status = future.result()
                if status == 1:
                    print("Failed - {}".format(id_))
            except Exception as exc:
                print('%r generated an exception: %s' % (id_, exc))
    

if __name__ == "__main__":
    update_ranking()