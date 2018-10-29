import abc

class UserDao(abc.ABC):


    @abc.abstractmethod
    def fetch_user_data(self, user_id):
        pass


    @abc.abstractmethod
    def create_user(self,user_id):
        pass


    @abc.abstractmethod
    def update_user_properties(self, user_id, new_values):
        pass
