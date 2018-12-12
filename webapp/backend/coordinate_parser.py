import push
from googlemaps import GoogleMaps

# Add coordinates to teacher and employer data

gmaps = GoogleMaps(api_key)

def getAllTeachersArrays():
	teachers = push.get_all_teachers()
	uids = teachers.keys()
	for uid in uids:
		teacher_dicts = getUpdatedTeacherDicts(teachers, uid)
		for teacher_dict in teacher_dicts:
			push.put_data_in_teachers(uid, teacher_dict) 

def getAllEmployersArrays():
	employers = push.get_all_employers()
	uids = employers.keys()
	for uid in uids:
		employer_dicts = getUpdatedEmployerDicts(teachers, uid)
		for employer_dict in employer_dicts:
			push.put_data_in_employers(uid, employer_dict) 


def getUpdatedTeacherDicts(teachers, uid):
	teachers = []
	for teacher in teachers:
		address = teacher['school_address']
		teacher['school_coordinate'] = getCoordinateFromAddress(address)
		teachers.append(teacher)
	return teacher_dicts

def getUpdatedEmployerDicts(employers, uid):
	employers = []
	for employer in employers:
		address = employer['address']
		employer['coordinate'] = getCoordinateFromAddress(address)
		employers.append(employer)

	return teacher_dicts

def getCoordinateFromAddress(address):
	address_str = address['street'] + ', ' + address['city'] ', ' + address['state'] + address['zip']
	lat, lng = gmaps.address_to_latlng(address_str)
	return lat, lng

if __name__ == "__main__":
	getAllTeacherArrays()
	getAllEmployerArrays()
