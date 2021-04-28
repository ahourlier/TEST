from .model import Comment

from flask_restx import Namespace

from .schema import CommentSchema

api = Namespace("Comment", description="Comments namespace")
