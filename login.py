import webapp2
import template_engine
import logging

class LoginPage(webapp2.RequestHandler):
    template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/login.html')

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        #logging.info(self.request.path)
        self.response.write(LoginPage.template.render({}))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        formName = self.request.get('form')
        if (formName == "login"):
            self.login()

    def login(self):
        email = self.request.get('email')
        password = self.request.get('password')
        template_values = {
            'email': email,
            'password': password,
        }
        self.response.write(LoginPage.template.render(template_values))


app = webapp2.WSGIApplication([
    ('/login', LoginPage)
],debug=True)
