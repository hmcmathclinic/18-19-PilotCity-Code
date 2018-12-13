import push
import googlemaps

# Add coordinates to teacher and employer data
keyFile = open('key.txt', 'r')
api_key = keyFile.read()
gmaps = googlemaps.Client(key=api_key)
#destination = '1060 Foster City Blvd, Foster City, CA 94404';
#distance = gmaps.distance_matrix(origin, destination); #for the future


def getAllTeachersArrays():
	teachers = push.get_all_teachers() #map with uid:data
	uids = teachers.keys() #array of uids
	for uid in uids:
		teacher_dict_new = getUpdatedTeacherDict(teachers[uid])
		push.put_data_in_teachers(uid, teacher_dict_new)


def getAllEmployersArrays():
	employers = push.get_all_employers()
	uids = employers.keys()
	for uid in uids:
		employer_dict_new = getUpdatedEmployerDict(employers[uid])
		push.put_data_in_employers(uid, employer_dict_new) 


def getUpdatedTeacherDict(teacher_dict):
	address = teacher_dict['school_address']
	lat,lng = getCoordinateFromAddress(address)
	coordinate = {}
	coordinate['lat'] = lat
	coordinate['lng'] = lng
	teacher_dict['coordinate'] = coordinate
	return teacher_dict

def getUpdatedEmployerDict(employer_dict):
	address = employer_dict['address']
	lat,lng = getCoordinateFromAddress(address)
	coordinate = {}
	coordinate['lat'] = lat
	coordinate['lng'] = lng
	employer_dict['coordinate'] = coordinate
	return employer_dict

def getCoordinateFromAddress(address):
	address_str = address['street'] + ', ' + address['city'] + ', ' + address['state'] + address['zip']
	geocode_result = gmaps.geocode(address_str)[0]["geometry"]["location"]
	# ^ returns {'lat': ###, 'lng': ###}
	return geocode_result["lat"], geocode_result["lng"]

if __name__ == "__main__":
	getAllTeachersArrays()
	getAllEmployersArrays()
