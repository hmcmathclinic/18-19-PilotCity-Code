import abc

class UserDao(abc.ABC):


    @abc.abstractmethod
    def fetch_employer_data(self, employer_id):
        pass


    @abc.abstractmethod
    def fetch_student_data(self, student_id):
        pass


    @abc.abstractmethod
    def fetch_teacher_data(self, teacher_id):
        pass