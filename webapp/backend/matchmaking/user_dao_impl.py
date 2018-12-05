from user_dao import UserDao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class UserDaoImpl(UserDao):
    

    def __init__(self):
        if (not len(firebase_admin._apps)):
            self.cred = credentials.Certificate('service_account.json') 
            default_app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()


    def fetch_employer_data(self, employer_id):
        employer_data = self.db.collection("employers_test").document(employer_id).get()
        # employer_data = db.reference('Employers/{0}'.format(employer_id)).get()
        return employer_data.to_dict()


    def fetch_teacher_data(self, teacher_id):
        teacher_data = self.db.collection("teachers_test").document(teacher_id).get()
        return teacher_data.to_dict()
    

    def fetch_student_data(self, student_id):
        student_data = self.db.collection("users").document(student_id).get()
        return student_data.to_dict()


    def fetch_all_teachers(self):
        out = []
        for doc in self.db.collection("teachers_test").get():
            out.append(doc.id)
        return out

    def fetch_all_employers(self):
        out = []
        for doc in self.db.collection("employers_test").get():
            out.append(doc.id)
        return out

