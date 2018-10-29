from user_dao import UserDao


class UserDaoImpl(UserDao):


    def fetch_user_data(self, user_id):
        print("Fetching user_data")


    def create_user(self,user_id):
        print("Creating user data in db")


    def update_user_properties(self, user_id, new_values):
        print("Updating user properties")

#test
user_dao = UserDaoImpl()
user_dao.create_user('1')
user_dao.fetch_user_data('1')
user_dao.update_user_properties('2', None)