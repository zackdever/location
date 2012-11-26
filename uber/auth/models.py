from flask.ext.login import UserMixin

class User(UserMixin):
    """Flask-Login compliant User."""
    def __init__(self, username, id):
        self.username = username
        self.id = id

    def is_active(self):
        """Determine if the user is active."""
        return True
