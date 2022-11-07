from fastapi_jwt_auth import AuthJWT

from app.models import UserAuth, User, RefreshToken, AccessToken
from app.exceptions import UserNotFoundError
from app.utils import PasswordService


class AuthController:
    def __init__(self):
        self._password_service: PasswordService = PasswordService()

    async def login(self, user_auth: UserAuth, auth: AuthJWT):
        user = await User.find_one(User.email == user_auth.email)
        if user is None:
            raise UserNotFoundError()
        if not self._password_service.verify_password(user_auth.password, user.password):
            raise UserNotFoundError()

        access_token = auth.create_access_token(subject=user.email)
        refresh_token = auth.create_refresh_token(subject=user.email)
        return RefreshToken(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, auth: AuthJWT):
        auth.jwt_refresh_token_required()
        access_token = auth.create_access_token(subject=auth.get_jwt_subject())
        return AccessToken(access_token=access_token)
