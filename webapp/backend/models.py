from google.appengine.ext import ndb
import logging

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

    @classmethod
    def entity_from_dict(cls, parent_key, data_dict):
        valid_properties = {}
        for cls_property in cls._properties:
            if cls_property in data_dict:
                valid_properties.update({cls_property: data_dict[cls_property]})
        #logging.info(valid_properties)
        # Update the id from the data_dict
        if 'id' in data_dict: # if creating a new entity
                valid_properties['id'] = data_dict['id']
        # Add the parent
        valid_properties['parent'] = parent_key
        try:
            entity = cls(**valid_properties)
        except Exception as e:
            logging.exception('Could not create entity \n' + repr(e))
        return entity


class TeacherUserData(ndb.Model):

    user_id = ndb.StringProperty()
    school_district_name = ndb.StringProperty()
    school_name = ndb.StringProperty()
    school_address = ndb.StringProperty()
    courses = ndb.StructuredProperty(Course, repeated=True)

    @classmethod
    def entity_from_dict(cls, parent_key, data_dict):
        valid_properties = {}
        for cls_property in cls._properties:
            if cls_property in data_dict:
                valid_properties.update({cls_property: data_dict[cls_property]})
        #logging.info(valid_properties)
        # Update the id from the data_dict
        if 'id' in data_dict: # if creating a new entity
                valid_properties['id'] = data_dict['id']
        # Add the parent
        valid_properties['parent'] = parent_key
        try:
            entity = cls(**valid_properties)
        except Exception as e:
            logging.exception('Could not create entity \n' + repr(e))
        return entity


class EmployerUserData(ndb.Model):

    user_id = ndb.StringProperty()
    company_name = ndb.StringProperty()
    liason_position = ndb.StringProperty()
    sectors = ndb.StringProperty(repeated=True)
    addresses = ndb.StructuredProperty(Address, repeated=True)

    @classmethod
    def entity_from_dict(cls, parent_key, data_dict):
        valid_properties = {}
        for cls_property in cls._properties:
            if cls_property in data_dict:
                valid_properties.update({cls_property: data_dict[cls_property]})
        #logging.info(valid_properties)
        # Update the id from the data_dict
        if 'id' in data_dict: # if creating a new entity
                valid_properties['id'] = data_dict['id']
        # Add the parent
        valid_properties['parent'] = parent_key
        try:
            entity = cls(**valid_properties)
        except Exception as e:
            logging.exception('Could not create entity \n' + repr(e))
        return entity


class StudentUserData(ndb.Model):
    user_id = ndb.StringProperty()
    school_district_name = ndb.StringProperty()
    school_name = ndb.StringProperty()
    grade_level = ndb.StringProperty()

    @classmethod
    def entity_from_dict(cls, parent_key, data_dict):
        valid_properties = {}
        for cls_property in cls._properties:
            if cls_property in data_dict:
                valid_properties.update({cls_property: data_dict[cls_property]})
        #logging.info(valid_properties)
        # Update the id from the data_dict
        if 'id' in data_dict: # if creating a new entity
                valid_properties['id'] = data_dict['id']
        # Add the parent
        valid_properties['parent'] = parent_key
        try:
            entity = cls(**valid_properties)
        except Exception as e:
            logging.exception('Could not create entity \n' + repr(e))
        return entity

