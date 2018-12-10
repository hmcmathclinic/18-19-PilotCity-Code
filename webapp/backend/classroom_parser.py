import push

def getAllClassroomArrays():
	teachers = push.get_all_teachers()
	uids = teachers.keys()
	for uid in uids:
		classroom_dicts = getClassroomDictFromArray(teachers[uid]['classes'], uid)
		i = 0
		for classroom_dict in classroom_dicts:
			push.put_data_in_classrooms(uid + str(i), classroom_dict) 
			i += 1


def getClassroomDictFromArray(classrooms, uid):
	classroom_dicts = []
	i = 0
	for classroom in classrooms:
		classroom_dict = classroom
		classroom_dict['teacher_uid'] = uid
		classroom_dict['uid'] = uid + str(i)
		i += 1
		classroom_dicts.append(classroom_dict)

	return classroom_dicts

if __name__ == "__main__":
	getAllClassroomArrays()


