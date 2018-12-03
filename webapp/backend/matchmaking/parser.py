import push

def getAllUserArrays():
	users = push.get_all_users()
	uids = users.keys()
	for uid in uids:
		if isEmployer(uid):
			User_dict, employer_dict = getEmployerDictFromArray(arr, uid)
			push.put_data_in_users(uid, User_dict) 
			push.put_data_in_employers(uid, employer_dict) 
		elif isTeacher(uid):
			User_dict, teacher_dict = getTeacherDictFromArray(arr, uid)
			push.put_data_in_users(uid, User_dict) 
			push.put_data_in_teachers(uid, teacher_dict) 

def isEmployer(arr):
	if "employer_story" in arr[0].keys():
		return True
	return False

def isTeacher(arr):
	if "teacher_story" in arr[0].keys():
		return True
	return False

def getEmployerDictFromArray(arr, uid):
	Users_dict = {}
	employer_dict = {}

	employer_story = arr[0]
	employer_address = arr[1]
	employer_sector = arr[2]
	employer_industry = arr[3]
	employer_solution_type = arr[4]
	employer_solution_keywords = arr[5]
	employer_question_keywords = arr[6]

	Users_dict["email"] = push.get_user_record(uid)
	Users_dict["first_name"] = employer_story["first_name"]
	Users_dict["isEmployer"] = True
	Users_dict["isStudent"] = False
	Users_dict["isTeacher"] = False
	Users_dict["last_name"] = employer_story["last_name"]
	Users_dict["phone"] = employer_story["phone"]

	employer_dict["company_name"] = employer_story["company_name"]
	employer_dict["address"] = employer_address
	employer_dict["isProduct"] = employer_solution_type["isProduct"]
	employer_dict["isService"] = employer_solution_type["isService"]
	employer_dict["keywords"] = employer_industry
	employer_dict["position_name"] = employer_story["position_name"]
	employer_dict["sector"] = employer_sector["sector"]

	return Users_dict, employers_dict

def getTeacherDictFromArray(arr, uid):
	Users_dict = {}
	teacher_dict = {}

	teacher_story = arr[0]
	teacher_address = arr[1]
	teacher_class = arr[2]
	teacher_ptype = arr[3]
	teacher_skills = arr[4]
	teacher_industry = arr[5]

	Users_dict["email"] = push.get_user_record(uid)
	Users_dict["first_name"] = teacher_story["first_name"]
	Users_dict["isEmployer"] = False
	Users_dict["isStudent"] = False
	Users_dict["isTeacher"] = True
	Users_dict["last_name"] = teacher_story["last_name"]
	Users_dict["phone"] = teacher_story["phone"]

	classes = []
	for bad_class in teacher_class:
		classroom = {}
		classroom["Grade"] = bad_class["Grade"]
		classroom["Period"] = bad_class["Period"]
		classroom["coursename"] = bad_class["Coursename"]
		classroom["schedule"] = getSchedule(bad_class, teacher_ptype)
		school_year = {}
		school_year["end"] = 2019
		school_year["start"] = 2018
		classroom["school_year"] = school_year
		classroom["semester"] = getSemester(bad_class["Semester"])
		classroom["students"] = bad_class["Students"]
		# Follow up and change this
		classroom["uid"] = uid
		classes = classes.append(classroom)
	teacher_dict["classes"] = classes
	teacher_dict["room_number"] = teacher_address.pop("room")
	teacher_dict["school_addresss"] = teacher_address
	teacher_dict["school_district"] = teacher_story["school_district"]
	teacher_dict["school_name"] = teacher_story["school_name"]
	teacher_dict["selected_industry_keywords"] = teacher_industry
	teacher_dict["selected_skills_keywords"] = teacher_skills

	return Users_dict, teacher_dict

def getSemester(n):
	if n == 0:
		return "Full Year"
	if n == 1:
		return "Fall"
	return "Spring" 

def getSchedule(bad_class, teacher_ptype):
	period = bad_class["Period"]
	schedule = {}

	for classroom in teacher_ptype:
		if classroom["period"] == period:
			for day in teacher_ptype["days"]:
				times = {}
				times["end_time"] = classroom["end_time"]
				times["start_time"] = classroom["start_time"]
				if day == "M":
					schedule["Monday"] = times
				elif day == "T":
					schedule["Tuesday"] = times
				elif day == "W":
					schedule["Wednesday"] = times
				elif day == "Th":
					schedule["Thursday"] = times
				else:
					schedule["Friday"] = times
	return schedule

if __name__ == "__main__":
	getAllUserArrays()


