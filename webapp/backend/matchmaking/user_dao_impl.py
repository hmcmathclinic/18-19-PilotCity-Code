from user_dao import UserDao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class UserDaoImpl(UserDao):
    

    def __init__(self):
        self.cred = credentials.Certificate('service_account.json')
        firebase_admin.initialize_app(self.cred, {
            'databaseURL' : 'https://test-database-5c3f8.firebaseio.com'
        })
        self.db = firestore.client()


    def fetch_employer_data(self, employer_id):
        employer_data = self.db.collection("users").document(employer_id).get()
        # employer_data = db.reference('Employers/{0}'.format(employer_id)).get()
        return employer_data.to_dict()


    def fetch_teacher_data(self, teacher_id):
        teacher_data = self.db.collection("users").document(teacher_id).get()
        return teacher_data.to_dict()
    

    def fetch_student_data(self, student_id):
        student_data = self.db.collection("users").document(student_id).get()
        return student_data.to_dict()


    def fetch_all_teachers(self):
        out = []
        for doc in self.db.collection("users").get():
            out.append(doc.to_dict())
        return out

