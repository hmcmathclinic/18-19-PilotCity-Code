import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('service_account.json') 
    default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def get_user_record(uid):
    user = auth.get_user(uid)
    return user.email


def get_all_users():
    out = {}
    users = db.collection("users").get()
    for user in users:
        out[user.id] = user.to_dict()
    return out

def get_all_teachers():
    out = {}
    teachers = db.collection("teachers").get()
    for teacher in teachers:
        out[teacher.id] = teacher.to_dict()
    return out

def get_all_employers():
    out = {}
    employers = db.collection("employers").get()
    for employer in employers:
        out[employer.id] = employer.to_dict()
    return out

def put_data_in_users(user_id, value):
    db.collection("Users").document(user_id).set(value)

def put_data_in_teachers(user_id, value):
    db.collection("teachers").document(user_id).set(value)

def put_data_in_employers(user_id, value):
    db.collection("employers").document(user_id).set(value)

def put_data_in_classrooms(user_id, value):
    db.collection("classroom").document(user_id).set(value)


# if __name__ == "__main__":
#     # get_user_record("49Z7lfsLuihpCaJUZBpuZ0g2rGt1")
