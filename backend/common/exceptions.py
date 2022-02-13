from werkzeug.exceptions import Unauthorized

class AuthError(Unauthorized):
    pass
