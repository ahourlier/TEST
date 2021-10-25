import os
import random
import string
from typing import List
from urllib.parse import urlencode

import requests
from firebase_admin import auth
from flask_sqlalchemy import Pagination
from googleapiclient.errors import HttpError
from sqlalchemy import or_

import logging

from .interface import PreferredAppInterface
from .model import PreferredApp
from app import db
from ..users.exceptions import UserNotFoundException
from ..users.model import User


class PreferredAppService:

    @staticmethod
    def create(new_attrs: PreferredAppInterface, user: User) -> PreferredApp:

        preferred_app = PreferredApp(**new_attrs)
        db.session.add(preferred_app)
        db.session.commit()

        current_user = User.query.filter_by(email=user.email).first()

        if not current_user:
            raise UserNotFoundException

        current_user.preferred_app_id = preferred_app.id
        db.session.commit()

        return preferred_app

    @staticmethod
    def get_by_id(preferred_app_id: int) -> PreferredApp:
        preferred_app = PreferredApp.query.get(preferred_app_id)
        if not preferred_app:
            raise UserNotFoundException
        return preferred_app

    @staticmethod
    def get_by_email(user_email: str) -> User:
        return PreferredApp.query.join(User).filter(User.email == user_email).first()
