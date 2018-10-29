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


    def update_user_properties(self, user_id, new_values):
        print("Updating user properties")

