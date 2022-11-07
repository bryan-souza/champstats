from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT

from app.models import UserAuth
from app.controllers import AuthController
from app.exceptions import NotFoundError

router = APIRouter(prefix='/auth')


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(user_auth: UserAuth, auth: AuthJWT = Depends(),
                auth_controller: AuthController = Depends(AuthController)):
    try:
        return await auth_controller.login(user_auth, auth)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Bad credentials')


@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh(auth: AuthJWT = Depends(), auth_controller: AuthController = Depends(AuthController)):
    return await auth_controller.refresh(auth)
