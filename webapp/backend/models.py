from google.appengine.ext import ndb


class Note(ndb.Model):
    """NDB model class for a user's note.

    Key is user id from decrypted token.
    """
    friendly_id = ndb.StringProperty()
    message = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)


class UserData(ndb.Model):
    """NDB model class for a user's note.

    Key is user id from decrypted token.
    """
    user_id = ndb.StringProperty()
    has_completed_form = ndb.BooleanProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
