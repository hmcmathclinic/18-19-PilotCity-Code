import push

def getAllUserArrays():
	users = push.get_all_users()
	uids = users.keys()
	for uid in uids:
		if isEmployer(users[uid]['form']):
			User_dict, employer_dict = getEmployerDictFromArray(users[uid]['form'], uid)
			push.put_data_in_users(uid, User_dict) 
			push.put_data_in_employers(uid, employer_dict) 
		elif isTeacher(users[uid]['form']):
			User_dict, teacher_dict = getTeacherDictFromArray(users[uid]['form'], uid)
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

	employer_story = arr[0]["employer_story"]
	employer_address = arr[1]["employer_address"]
	employer_sector = arr[2]["employer_sector"]
	employer_industry = arr[3]["employer_industry"]
	employer_solution_type = arr[4]["employer_solution_type"]
	employer_solution_keywords = arr[5]["employer_solution_keywords"]
	employer_question_keywords = arr[6]["employer_question_keywords"]

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
	employer_dict["position_name"] = employer_story["position_name"]
	employer_dict["sector"] = employer_sector["sector"]
	employer_dict["selected_challenge_keywords"] = employer_question_keywords["selected_question_keywords"]
	employer_dict["selected_industry_keywords"] = employer_industry
	employer_dict["selected_product_keywords"] = employer_solution_keywords["selected_product_keywords"]
	employer_dict["selected_service_keywords"] = employer_solution_keywords["selected_service_keywords"]

	return Users_dict, employer_dict

def getTeacherDictFromArray(arr, uid):
	Users_dict = {}
	teacher_dict = {}

	teacher_story = arr[0]["teacher_story"]
	teacher_address = arr[1]["teacher_address"]
	if "teacher_class" in arr[2]:
		teacher_class = arr[2]["teacher_class"]
		teacher_ptype = arr[3]["teacher_ptype"]
		teacher_skills = arr[4]["teacher_skills"]
		teacher_industry = arr[5]["teacher_industry"]

	else:
		teacher_class = []
		teacher_ptype = arr[2]["teacher_ptype"]
		teacher_skills = arr[3]["teacher_skills"]
		teacher_industry = arr[4]["teacher_industry"]
	
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
		classes.append(classroom)
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
	period = 'P' + bad_class["Period"]
	schedule = []

	for classroom in teacher_ptype:
		this_class_schedule = {}
		if classroom["period"] == period:
			days = classroom['days']
			for day in days:
				times = {}
				times['end_time'] = classroom["end_time"]
				times['start_time'] = classroom["start_time"]
				this_class_schedule[day] = times
		schedule.append(this_class_schedule)
				
	return schedule

if __name__ == "__main__":
	getAllUserArrays()


