import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.server import app
from app.models import User, RefreshToken, AccessToken
from app.controllers import AuthController
from app.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    AccountDisabledError,
    EmailNotVerifiedError
)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_register(client, monkeypatch):
    test_data = User(_id='636d8e4959317d937f9eda82',
                     disabled=False,
                     email='johndoe@example.com',
                     email_confirmed_at=datetime(2022, 1, 1, 10, 39, 00),
                     first_name='John',
                     last_name='Doe',
                     password='$2b$12$mPSqPuD38jEsuPIz2GM4.upZiJmB1dATAufKJUltIenWRoLVnx6CC')

    async def mock_register_new_user(*args, **kwargs):
        return test_data

    monkeypatch.setattr(AuthController, 'register_new_user', mock_register_new_user)

    response = client.post('/auth/register',
                           json={'email': 'johndoe@example.com', 'password': 'unhashedpassword'})
    assert response.status_code == 200
    assert response.json() == {
        '_id': '636d8e4959317d937f9eda82',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'disabled': False,
        'password': '$2b$12$mPSqPuD38jEsuPIz2GM4.upZiJmB1dATAufKJUltIenWRoLVnx6CC',
        'email_confirmed_at': '2022-01-01T10:39:00'
    }

    monkeypatch.delattr(AuthController, 'register_new_user')


def test_register_409(client, monkeypatch):
    async def mock_register_new_user_409(*args, **kwargs):
        raise UserAlreadyExistsError()

    monkeypatch.setattr(AuthController, 'register_new_user', mock_register_new_user_409)

    response = client.post('/auth/register',
                           json={'email': 'johndoe@example.com', 'password': 'unhashedpassword'})
    assert response.status_code == 409

    monkeypatch.delattr(AuthController, 'register_new_user')


def test_login(client, monkeypatch):
    test_data = RefreshToken(access_token='finge_que_tem_um_token_jwt_aqui',
                             refresh_token='finge_que_tem_outro_token_jwt_aqui')

    async def mock_login(*args, **kwargs):
        return test_data

    monkeypatch.setattr(AuthController, 'user_login', mock_login)

    response = client.post('/auth/login',
                           json={'email': 'johndoe@example.com', 'password': 'unhashedpassword'})
    assert response.status_code == 200
    assert response.json() == {
        'access_token': 'finge_que_tem_um_token_jwt_aqui',
        'access_token_expires': 900,
        'refresh_token': 'finge_que_tem_outro_token_jwt_aqui',
        'refresh_token_expires': 2592000
    }

    monkeypatch.delattr(AuthController, 'user_login')


def test_login_401(client, monkeypatch):
    async def mock_login_401(*args, **kwargs):
        raise UserNotFoundError()

    monkeypatch.setattr(AuthController, 'user_login', mock_login_401)

    response = client.post('/auth/login',
                           json={'email': 'johndoe@example.com', 'password': 'unhashedpassword'})
    assert response.status_code == 401

    monkeypatch.delattr(AuthController, 'user_login')


def test_refresh(client, monkeypatch):
    test_data = AccessToken(access_token='finge_que_tem_um_token_jwt_aqui')

    async def mock_refresh_access_token(*args, **kwargs):
        return test_data

    monkeypatch.setattr(AuthController, 'refresh_access_token', mock_refresh_access_token)

    response = client.post('/auth/refresh',
                           headers={'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbG'})
    assert response.status_code == 200
    assert response.json() == {'access_token': 'finge_que_tem_um_token_jwt_aqui',
                               'access_token_expires': 900}

    monkeypatch.delattr(AuthController, 'refresh_access_token')


def test_forgot_password(client, monkeypatch):
    async def mock_forgot_password(*args, **kwargs):
        return None

    monkeypatch.setattr(AuthController, 'forgot_password', mock_forgot_password)

    response = client.post('/auth/forgot-password', json={'email': 'johndoe@example.com'})
    assert response.status_code == 200

    monkeypatch.delattr(AuthController, 'forgot_password')


def test_forgot_password_400_email_not_verified(client, monkeypatch):
    async def mock_forgot_password(*args, **kwargs):
        raise EmailNotVerifiedError('johndoe@example.com')

    monkeypatch.setattr(AuthController, 'forgot_password', mock_forgot_password)

    response = client.post('/auth/forgot-password', json={'email': 'johndoe@example.com'})
    assert response.status_code == 400

    monkeypatch.delattr(AuthController, 'forgot_password')


def test_forgot_password_400_account_disabled(client, monkeypatch):
    async def mock_forgot_password(*args, **kwargs):
        raise AccountDisabledError('123')

    monkeypatch.setattr(AuthController, 'forgot_password', mock_forgot_password)

    response = client.post('/auth/forgot-password', json={'email': 'johndoe@example.com'})
    assert response.status_code == 400

    monkeypatch.delattr(AuthController, 'forgot_password')


def test_reset_password(client, monkeypatch):
    test_data = User(_id='636d8e4959317d937f9eda82', first_name='John', last_name='Doe',
                     email='johndoe@example.com', disabled=False, password='random-hash-here',
                     email_confirmed_at=datetime(2022, 1, 1, 10, 39, 00))

    async def mock_reset_password(*args, **kwargs):
        return test_data

    monkeypatch.setattr(AuthController, 'reset_password', mock_reset_password)

    response = client.post('/auth/reset-password/finge=que-tem-um-token-jwt-aqui',
                           json={'new_password': 'unhashedpassword2'})
    assert response.status_code == 200
    assert response.json() == {
        '_id': '636d8e4959317d937f9eda82',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'disabled': False,
        'password': 'random-hash-here',
        'email_confirmed_at': '2022-01-01T10:39:00'
    }

    monkeypatch.delattr(AuthController, 'reset_password')


def test_reset_password_400_email_not_verified(client, monkeypatch):
    async def mock_forgot_password(*args, **kwargs):
        raise EmailNotVerifiedError('johndoe@example.com')

    monkeypatch.setattr(AuthController, 'reset_password', mock_forgot_password)

    response = client.post('/auth/reset-password/finge-que-tem-um-token-jwt-aqui',
                           json={'new_password': 'unhashedpassword2'})
    assert response.status_code == 400

    monkeypatch.delattr(AuthController, 'reset_password')


def test_reset_password_400_account_disabled(client, monkeypatch):
    async def mock_forgot_password(*args, **kwargs):
        raise AccountDisabledError('123')

    monkeypatch.setattr(AuthController, 'reset_password', mock_forgot_password)

    response = client.post('/auth/reset-password/finge-que-tem-um-token-jwt-aqui',
                           json={'new_password': 'unhashedpassword2'})
    assert response.status_code == 400

    monkeypatch.delattr(AuthController, 'reset_password')
