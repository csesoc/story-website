from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, InternalServerError

class IncorrectError(Exception):
    def __init__(self, description):
        super().__init__()
        self.description = description

class RequestError(BadRequest):
    pass

class AuthError(Unauthorized):
    pass

class AccessError(Forbidden):
    pass

class InvalidError(InternalServerError):
    pass
