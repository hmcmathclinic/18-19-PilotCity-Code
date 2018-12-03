import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


cred = credentials.Certificate('service_account.json')
firebase_admin.initialize_app(cred, options={
    'databaseURL': 'https://my-project-id.firebaseio.com'
})
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


def put_data_in_users(user_id, value):
    db.collection("Users_test").document(user_id).set(value)


def put_data_in_teachers(user_id, value):
    db.collection("teachers_test").document(user_id).set(value)


def put_data_in_employers(user_id, value):
    db.collection("employers_test").document(user_id).set(value)


if __name__ == "__main__":
    get_user_record("49Z7lfsLuihpCaJUZBpuZ0g2rGt1")