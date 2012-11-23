from flask.ext.login import UserMixin

class User(UserMixin):
    def __init__(self, username, id):
        self.username = username
        self.id = id

    def is_active(self):
        return True
