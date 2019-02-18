import webapp2
import template_engine
from google.appengine.api import users
from google.appengine.ext import ndb
from userModel import UserModel
import logging

class HomePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/home.html')
        user = users.get_current_user()
        logging.info(user)
        url = ''
        url_string = ''
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_key = ndb.Key('UserModel', user.email())
            myuser = myuser_key.get()
            logging.info(myuser)
            if myuser == None:
                welcome = 'Welcome to the application'
                logging.info(welcome)
                logging.info(user)
                myuser = UserModel(id=user.email(), email = user.email())
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
        }
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', HomePage)
])
