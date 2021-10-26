from .interface import PreferredAppInterface
from .model import PreferredApp
from app import db
from .exceptions import PreferredAppNotFoundException
from ..users.exceptions import UserNotFoundException
from ..users.model import User


class PreferredAppService:

    @staticmethod
    def create(new_attrs: PreferredAppInterface) -> PreferredApp:

        preferred_app = PreferredApp(**new_attrs)
        db.session.add(preferred_app)
        db.session.commit()

        return preferred_app

    @staticmethod
    def create_for_user(new_attrs: PreferredAppInterface, user_id) -> User:

        preferred_app = PreferredAppService.create(new_attrs)

        db_user = User.query.filter_by(id=user_id).first()

        if not db_user:
            raise UserNotFoundException

        db_user.preferred_app_id = preferred_app.id
        db.session.commit()

        return db_user

    @staticmethod
    def update(preferred_app_id: int, new_attrs: PreferredAppInterface):
        db_preferred_app = PreferredApp.query.filter_by(id=preferred_app_id).first()

        if not db_preferred_app:
            raise PreferredAppNotFoundException

        db_preferred_app.update(new_attrs)
        db.session.commit()

        return db_preferred_app

    @staticmethod
    def delete(preferred_app_id: int):

        preferred_app_query = PreferredApp.query.filter_by(id=preferred_app_id)

        if not preferred_app_query.first():
            raise PreferredAppNotFoundException

        preferred_app_query.delete()
        db.session.commit()

        return preferred_app_id

    @staticmethod
    def get_my_preferred_app(user: User):
        return user.preferred_app

    # @staticmethod
    # def get_by_id(preferred_app_id: int) -> PreferredApp:
    #     preferred_app = PreferredApp.query.get(preferred_app_id)
    #     if not preferred_app:
    #         raise UserNotFoundException
    #     return preferred_app
    #
    # @staticmethod
    # def get_by_email(user_email: str) -> User:
    #     return PreferredApp.query.join(User).filter(User.email == user_email).first()
