from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr

from app.models import UserAuth, User, RefreshToken, AccessToken
from app.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    AccountDisabledError,
    EmailNotVerifiedError
)
from app.utils import PasswordService, MailingService


class AuthController:
    def __init__(self):
        self._password_service: PasswordService = PasswordService()
        self._mailing_service: MailingService = MailingService()

    async def register_new_user(self, user_auth: UserAuth):
        user = await User.find_one(User.email == user_auth.email)
        if user is not None:
            raise UserAlreadyExistsError()

        hashed_password = self._password_service.hash_password(user_auth.password)
        user = User(email=user_auth.email, password=hashed_password)
        await user.create()
        return user

    async def user_login(self, user_auth: UserAuth, auth: AuthJWT):
        user = await User.find_one(User.email == user_auth.email)
        if user is None:
            raise UserNotFoundError()
        if not self._password_service.verify_password(user_auth.password, user.password):
            raise UserNotFoundError()

        access_token = auth.create_access_token(subject=user.email)
        refresh_token = auth.create_refresh_token(subject=user.email)
        return RefreshToken(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, auth: AuthJWT):
        access_token = auth.create_access_token(subject=auth.get_jwt_subject())
        return AccessToken(access_token=access_token)

    async def forgot_password(self, email: EmailStr, auth: AuthJWT):
        user = await User.find_one(User.email == email)
        if user.email_confirmed_at is None:
            raise EmailNotVerifiedError(user.email)
        if user.disabled:
            raise AccountDisabledError(user.id)

        token = auth.create_access_token(subject=user.email)
        await self._mailing_service.send_password_reset_email(email, token)
        return None

    async def reset_password(self, token: str, new_password: str, auth: AuthJWT):
        auth._token = token
        user = await User.find_one(User.email == auth.get_jwt_subject())
        if user.email_confirmed_at is None:
            raise EmailNotVerifiedError(user.email)
        if user.disabled:
            raise AccountDisabledError(user.id)

        user.password = self._password_service.hash_password(new_password)
        await user.save()
        return user
