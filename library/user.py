from google.appengine.api import users
from google.appengine.ext import ndb
from models.userModel import UserModel


class User:
    @classmethod
    def get_user(cls, current_user):

        user = users.get_current_user()
        url = ''
        url_string = ''
        if user:
            url = users.create_logout_url(current_user.request.uri)
            url_string = 'Logout'
            myuser_key = ndb.Key('UserModel', user.email())
            myuser = myuser_key.get()
            if myuser == None:
                myuser = UserModel(id=user.email(), email=user.email())
                myuser.put()
        else:
            url = users.create_login_url(current_user.request.uri)
            url_string = 'login'

        data = {
            'url': url,
            'url_string': url_string,
            'user': user,
        }
        return data
