from werkzeug.exceptions import Unauthorized, InternalServerError

class AuthError(Unauthorized):
    pass

class InvalidError(InternalServerError):
    pass
