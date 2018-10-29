import abc

class UserDao(abc.ABC):
    @abc.abstractmethod
    def funcname(self, parameter_list):
        pass