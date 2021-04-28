from .model import User, UserGroup

from flask_restx import Namespace
from .schema import UserSchema

api = Namespace("Users", description="Users namespace")
