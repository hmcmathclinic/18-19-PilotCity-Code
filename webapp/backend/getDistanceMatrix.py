import googlemaps
from user_dao_impl import UserDaoImpl

keyFile = open('key.txt', 'r')
api_key = keyFile.read()
gmaps = googlemaps.Client(key=api_key)
dao = UserDaoImpl()
all_employers = dao.fetch_all_employers()
employer_ids = list(all_employers.keys())
all_teachers = dao.fetch_all_teachers()
teacher_ids = list(all_teachers.keys())


origins = ""
dests = ""
for teacher_id in teacher_ids:
    teacher_data = all_teachers[teacher_id]
    teacher_coord = teacher_data["coordinate"]
    dests+=(str(teacher_coord["lat"]) + "," + str(teacher_coord["lng"]))+"|"
dests = dests[:-1]
for employer_id in employer_ids:
        employer_data = all_employers[employer_id]
        emp_coord = employer_data["coordinate"]
        origins+= (str(emp_coord["lat"]) + "," + str(emp_coord["lng"]))+"|"
origins = origins[:-1]
print(origins)
print("-------")
print(dests)   
rows = gmaps.distance_matrix(origins, dests)['rows']
print(rows[0])
  