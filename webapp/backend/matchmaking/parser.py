
def arrayToDictionary(user_id):
	# get data
	arr = []
	if isEmployer(user_id):
		return getEmployerDictFromArray(arr), user_id
	elif isTeacher(user_id):
		return getTeacherDictFromArray(arr), user_id

def isEmployer(arr):
	if "employer_story" in arr[0].keys():
		return True
	return False

def isTeacher(arr):
	if "teacher_story" in arr[0].keys():
		return True
	return False

def getEmployerDictFromArray(arr):
	Users_dict = {}
	employers_dict = {}

	employer_story = arr[0]
	employer_address = arr[1]
	employer_sector = arr[2]
	employer_industry = arr[3]
	employer_solution_type = arr[4]
	employer_solution_keywords = arr[5]
	employer_question_keywords = arr[6]

	# Users_dict["email"] = figure out
	Users_dict["first_name"] = employer_story["first_name"]
	Users_dict["isEmployer"] = True
	Users_dict["isStudent"] = False
	Users_dict["isTeacher"] = False
	Users_dict["last_name"] = employer_story["last_name"]
	Users_dict["phone"] = employer_story["phone"]

	employers_dict["company_name"] = employer_story["company_name"]
	employers_dict["position_name"] = employer_story["position_name"]
	employers_dict["address"] = employer_address
	employers_dict["isProduct"] = employer_solution_type["isProduct"]
	employers_dict["isService"] = employer_solution_type["isService"]
	employers_dict[]


	return 0

def getTeacherDictFromArray(arr):
	return 0