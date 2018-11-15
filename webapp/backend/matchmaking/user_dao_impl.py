from user_dao import UserDao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class UserDaoImpl(UserDao):
    

    def __init__(self):
        self.cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(self.cred, {
            'databaseURL' : 'https://test-database-5c3f8.firebaseio.com'
        })
        self.root = db.reference()


    def fetch_employer_data(self, employer_id):
        employer_data = db.reference('Employers/{0}'.format(employer_id)).get()
        return employer_data


    def fetch_teacher_data(self, teacher_id):
        teacher_data = db.reference('Teachers/{0}'.format(teacher_id)).get()
        return teacher_data
    

    def fetch_student_data(self, student_id):
        student_data = db.reference('Students/{0}'.format(student_id)).get()
        return student_data


