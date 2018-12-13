import googlemaps

keyFile = open('key.txt', 'r')
api_key = keyFile.read()
gmaps = googlemaps.Client(key=api_key)

def getDistanceList(self):
    origins = []
    dests = []
    for teacher_id in self.teacher_ids:
        for employer_id in self.employer_ids:
                teacher_data = self.all_teachers[teacher_id]
                employer_data = self.all_employers[employer_id]
                emp_coord = employer_data["coordinate"]
                teacher_coord = teacher_data["coordinate"]
                origins.append(str(emp_coord["lat"]) + "," + str(emp_coord["lng"]))
                dests.append(str(teacher_coord["lat"]) + "," + str(teacher_coord["lng"]))
    rows = gmaps.distance_matrix(origins, dests)['rows']
    return rows[0]