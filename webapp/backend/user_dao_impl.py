from user_dao import UserDao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class UserDaoImpl(UserDao):
    

    def __init__(self):
        if (not len(firebase_admin._apps)):
            self.cred = credentials.Certificate('matchmaking/service_account.json') 
            firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()


    def fetch_employer_data(self, employer_id):
        employer_data = self.db.collection("employers").document(employer_id).get()
        # employer_data = db.reference('Employers/{0}'.format(employer_id)).get()
        return employer_data.to_dict()


    def fetch_teacher_data(self, teacher_id):
        teacher_data = self.db.collection("teachers").document(teacher_id).get()
        return teacher_data.to_dict()

    def fetch_classroom_data(self, classroom_id):
        classroom_data = self.db.collection("classroom").document(classroom_id).get()
        return classroom_data.to_dict()
    

    def fetch_student_data(self, student_id):
        student_data = self.db.collection("students").document(student_id).get()
        return student_data.to_dict()


    def fetch_all_teachers(self):
        out = []
        for doc in self.db.collection("teachers").get():
            out.append(doc.id)
        return out

    def fetch_all_employers(self):
        out = []
        for doc in self.db.collection("employers").get():
            out.append(doc.id)
        return out

    def fetch_all_classrooms(self):
        out = []
        for doc in self.db.collection("classroom").get():
            out.append(doc.id)
        return out
