import webapp2
import template_engine


class HomePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/home.html')

        self.response.write(template.render({}))


app = webapp2.WSGIApplication([
    ('/', HomePage)
])
