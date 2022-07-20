<<<<<<< HEAD
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from models.user import User

# JWT plugin

jwt = JWTManager()

@jwt.user_lookup_loader
def user_lookup(_, payload):
    return User.get(payload["sub"])

@jwt.user_identity_loader
def user_identity(user):
    return user.id

# Mail plugin

mail = Mail()
=======
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from models.user import User

# JWT plugin

jwt = JWTManager()

@jwt.user_lookup_loader
def user_lookup(_, payload):
    return User.get(payload["sub"])

@jwt.user_identity_loader
def user_identity(user):
    return user.id

# Mail plugin

mail = Mail()
>>>>>>> ffb4c6ef4ed862c6fec20a1167c30d75808de300
