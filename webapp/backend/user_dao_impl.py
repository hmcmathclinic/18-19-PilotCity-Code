from user_dao import UserDao
from google.appengine.ext import ndb
from models import BasicUserData, StudentUserData, EmployerUserData, TeacherUserData


class UserDaoImpl(UserDao):

    
    def __fetch_data_from_given_table(self, user_id, table_class_name):
        ancestor_key = ndb.Key(table_class_name, user_id)
        basic_data_query = table_class_name.query(ancestor=ancestor_key).order(-table_class_name.created)
        basic_user_data = basic_data_query.fetch()
        if basic_user_data:
            return basic_user_data[0]
        return None


    def fetch_user_data(self, user_id):
        user_data = {}
        basic_data = self.__fetch_data_from_given_table(user_id, BasicUserData)
        if not basic_data:
            return basic_data

        user_data.update(basic_data.to_dict())
        additional_data = None

        if user_data["user_type"] == "Student":
            additional_data = self.__fetch_data_from_given_table(user_id, StudentUserData)
        elif user_data["user_type"] == "Teacher":
            additional_data = self.__fetch_data_from_given_table(user_id, TeacherUserData)
        else:
            additional_data = self.__fetch_data_from_given_table(user_id, EmployerUserData)

        if additional_data:
            user_data.update(additional_data.to_dict())

        return user_data


    def create_user(self,user_id, new_values):
        print("Creating user data in db")
        key = ndb.key(BasicUserData, user_id)
        query_count = BasicUserData.query(key).count(keys_only=True)
        if query_count > 0:
            return False
        basic_data_entry = BasicUserData(parent=ndb.Key(BasicUserData, user_id))
        basic_data_entry.user_id = user_id
        basic_data_entry.put()
        if "user_type" in new_values:
            basic_data_entry.user_type = new_values["user_type"]
            if new_values["user_type"] == "Teacher":
                entry_in_teacherdb = TeacherUserData(parent=ndb.Key(TeacherUserData, user_id))
                entry_in_teacherdb.user_id = user_id
                entry_in_teacherdb.put()
            elif new_values["user_type"] == "Student":
                entry_in_studentdb = StudentUserData(parent=ndb.Key(StudentUserData, user_id))
                entry_in_studentdb.user_id = user_id
                entry_in_studentdb.put()
            elif new_values["user_type"] == "Employer":
                entry_in_employerdb = EmployerUserData(parent=ndb.Key(EmployerUserData, user_id))
                entry_in_employerdb.user_id = user_id
                entry_in_employerdb.put()
        self.update_user_properties(user_id, new_values)
        return True


    def update_user_properties(self, user_id, new_values):
        basic_user_data = self.__fetch_data_from_given_table(user_id, BasicUserData)
        if not basic_user_data:
            return False

        if basic_user_data.user_type == "Student":
            key = ndb.key(StudentUserData, user_id)
            additional_entity = StudentUserData.entity_from_dict(parent_key=key, data_dict=new_values)
        elif basic_user_data.user_type == "Teacher":
            key = ndb.key(TeacherUserData, user_id)
            additional_entity = TeacherUserData.entity_from_dict(parent_key=key, data_dict=new_values)
        else:
            key = ndb.key(EmployerUserData, user_id)
            additional_entity = EmployerUserData.entity_from_dict(parent_key=key, data_dict=new_values)
        if additional_entity:
            additional_entity.put()
            basic_data_key = ndb.key(BasicUserData, user_id)
            basic_data_entity = BasicUserData.entity_from_dict(parent_key=basic_data_key, data_dict=new_values)
            basic_data_entity.put()

        return True
