from google.appengine.ext import ndb

class UserModel(ndb.Model):
    email = ndb.StringProperty()