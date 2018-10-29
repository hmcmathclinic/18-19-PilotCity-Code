from google.appengine.ext import ndb


class Address(ndb.Model):
    address_type = ndb.StringProperty()  # E.g., 'home', 'work'
    street = ndb.StringProperty()
    city = ndb.StringProperty()
    is_headquarters = ndb.BooleanProperty()

class Course(ndb.Model):
    course_name = ndb.StringProperty()
    room_number = ndb.IntegerProperty()
    course_duration = ndb.IntegerProperty()
    number_of_students = ndb.IntegerProperty()
    grade_level = ndb.StringProperty()


class BasicUserData(ndb.Model):
    """NDB model class for a user's note.

    Key is user id from decrypted token.
    """
    user_id = ndb.StringProperty()
    user_type = ndb.StringProperty()
    has_completed_onboarding = ndb.BooleanProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    email_address = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)


class TeacherUserData(ndb.Model):
    user_id = ndb.StringProperty()
    school_district_name = ndb.StringProperty()
    school_name = ndb.StringProperty()
    school_address = ndb.StringProperty()
    courses = ndb.StructuredProperty(Course, repeated=True)


class EmployerUserData(ndb.Model):
    user_id = ndb.StringProperty()
    company_name = ndb.StringProperty()
    liason_position = ndb.StringProperty()
    sectors = ndb.StringProperty(repeated=True)
    addresses = ndb.StructuredProperty(Address, repeated=True)


class StudentUserData(ndb.Model):
    user_id = ndb.StringProperty()
    school_district_name = ndb.StringProperty()
    school_name = ndb.StringProperty()
    grade_level = ndb.StringProperty()


