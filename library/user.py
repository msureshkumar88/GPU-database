from google.appengine.api import users


class User:
    @classmethod
    def get_user(cls,current_user):

        user = users.get_current_user()
        url = ''
        url_string = ''
        if user:
            url = users.create_logout_url(current_user.request.uri)
            url_string = 'logout'
        else:
            url = users.create_login_url(current_user.request.uri)
            url_string = 'login'

        data = {
            'url': url,
            'url_string': url_string,
            'user': user,
        }
        return data
