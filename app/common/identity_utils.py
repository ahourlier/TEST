import logging
import os
import random
import string

import requests
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError

from flask import current_app
from requests import HTTPError

from app.auth.users.interface import UserInterface


class IdentityUtils:
    @staticmethod
    def create_user(user: UserInterface) -> str:
        pwd = "".join(random.choice(string.ascii_lowercase) for _ in range(6))
        user = auth.create_user(
            email=user["email"],
            email_verified=False,
            password=pwd,
            display_name=f"{user['first_name']} {user['last_name']}",
            disabled=False,
        )
        return user.uid

    @staticmethod
    def delete_user(uid: str):
        try:
            auth.delete_user(uid)
        except UserNotFoundError:
            pass

    @staticmethod
    def send_reset_password_email(user_email):
        try:
            requests.post(
                f"{current_app.config['IDENTITY_TOOLKIT_API_BASE_URL']}accounts:sendOobCode?key={os.environ.get('IDENTITY_PLATFORM_API_KEY')}",
                json=dict(requestType="PASSWORD_RESET", email=user_email),
            )
        except HTTPError as e:
            logging.error(
                f"An error occurred while sending reset password email to {user_email}: {e} "
            )
