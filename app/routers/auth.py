from fastapi import APIRouter, Depends, HTTPException, Body, Response
from fastapi import status
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr

from app.models import UserAuth
from app.controllers import AuthController
from app.exceptions import (
    NotFoundError,
    UserAlreadyExistsError,
    AccountDisabledError,
    EmailNotVerifiedError
)

router = APIRouter(prefix='/auth')


@router.post('/register', status_code=status.HTTP_200_OK)
async def register(user_auth: UserAuth, auth_controller: AuthController = Depends(AuthController)):
    try:
        return await auth_controller.register_new_user(user_auth)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists")


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(user_auth: UserAuth, auth: AuthJWT = Depends(),
                auth_controller: AuthController = Depends(AuthController)):
    try:
        return await auth_controller.user_login(user_auth, auth)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Bad credentials')


@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh(auth: AuthJWT = Depends(), auth_controller: AuthController = Depends(AuthController)):
    return await auth_controller.refresh_access_token(auth)


@router.post('/forgot-password', status_code=status.HTTP_200_OK)
async def forgot_password(email: EmailStr = Body(..., embed=True), auth: AuthJWT = Depends(),
                          auth_controller: AuthController = Depends(AuthController)):
    try:
        await auth_controller.forgot_password(email, auth)
        return Response(status_code=status.HTTP_200_OK)
    except EmailNotVerifiedError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already verified")
    except AccountDisabledError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Account disabled")


@router.post('/reset-password/{token}', status_code=status.HTTP_200_OK)
async def reset_password(token: str, new_password: str = Body(..., embed=True),
                         auth: AuthJWT = Depends(),
                         auth_controller: AuthController = Depends(AuthController)):
    try:
        return await auth_controller.reset_password(token, new_password, auth)
    except EmailNotVerifiedError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already verified")
    except AccountDisabledError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Account disabled")
