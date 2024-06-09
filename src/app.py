from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Generic, Optional, TypeVar, Annotated
from enum import Enum
from datetime import datetime
from jose import jws

app = FastAPI()

T = TypeVar("T")

class PaginationResp(BaseModel, Generic[T]):
    items: list[T]
    cursor: int
    page: int
    pages: int
    total: int


class UserRole(Enum):
    ADMIN = 'admin'
    MASTER = 'master'

class User(BaseModel):
    username: str
    role: UserRole
    createdAt: int
    firstName: str
    lastName: str

class UserAuth(BaseModel):
    username: str
    password: str

class UserRegisterMeta(User):
    username: Optional[str] = None
    role: Optional[UserRole] = None
    createdAt: Optional[int] = None

class UserRegister(BaseModel):
    auth: UserAuth
    meta: UserRegisterMeta

class SetPasswordData(BaseModel):
    username: str
    currentPassword: str
    password: str
    passwordRepeat: str

# just state, need change to real DB
USERS_DB: dict[str, User] = {
    "admin": User(username='admin', role=UserRole.ADMIN, createdAt=int(datetime.now().timestamp()), firstName='admin', lastName='admin')
}
USERS_AUTH_DB: dict[str, UserAuth] = {}

# just state, need change to real DB
# USERS_AUTH_STATE: list[str] = []

# def check_logged_in(check_username: str):
#     return next((username for username in USERS_AUTH_STATE if username == check_username), None)

@app.get('/api/users', response_model=PaginationResp[User])
async def get_users():
    return {
        'items': USERS_DB.values(),
        'cursor': 0,
        'page': 1,
        'pages': 1,
        'total': len(USERS_DB)
    }

@app.post('/api/users', response_model=User)
async def register_user(userData: UserRegister):
    auth, meta = userData.auth, userData.meta

    userAuth = UserAuth(
        username=auth.username,
        password=auth.password
    )

    # check
    # if (meta.role != None && userAuth?.role !== UserRole.ADMIN)
        # throw JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f'Not enough rights')

    user = User(
        username=auth.username,
        role=meta.role or UserRole.MASTER,
        createdAt=int(datetime.now().timestamp()),
        firstName=meta.firstName,
        lastName=meta.lastName
    )

    USERS_AUTH_DB[auth.username] = userAuth
    USERS_DB[auth.username] = user

    # USERS_AUTH_STATE.append(auth.username)

    return user

@app.post('/api/users/login', response_model=User)
async def login_user(userAuth: UserAuth):
    username, password = userAuth.username, userAuth.password

    userAuthData = USERS_AUTH_DB.get(username)

    if (userAuthData is None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f'User ({username}) does not exist')

    if (userAuthData.password != password):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f'Incorrect credentials')

    userData = USERS_DB.get(username)
    assert userData is not None

    return userData

@app.get('/api/users/logout', status_code=204)
async def logout_user():
    # remove from dict
    pass

@app.get('/api/users/u/{username}', response_model=User)
async def get_user(username: str):
    user = USERS_DB.get(username)

    if (user is None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f'User ({username}) does not exist')

    return user

@app.delete('/api/users/u/{username}', status_code=204)
async def delete_user(username: str):
    user = USERS_DB.get(username)

    if (user is None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f'User ({username}) does not exist')

    USERS_DB.pop(username)
    pass

@app.patch('/api/users/u/{username}/password', status_code=204)
async def update_password_user(username: str, passwordData: SetPasswordData):
    userAuthData = USERS_AUTH_DB.get(username)

    if (userAuthData is None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f'User ({username}) does not exist')

    # check
    # if (userAuth.username !== username && userAuth.role !== UserRole.ADMIN)
        # throw JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f'Not enough rights')

    if (passwordData.currentPassword != userAuthData.password):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f'Incorrect credentials')

    if (passwordData.password == userAuthData.password):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f'Password matches with current')

    if (passwordData.currentPassword != passwordData.passwordRepeat):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f'New passwords do not match')

    userAuthData.password = passwordData.password

    pass


class Engine(BaseModel):
    id: str
    humanId: int
    createdAt: int
    maxSpeedPm: int
    nominalVoltage: int
    nominalCurrent: int
    weight: int

ENGINES_DB: dict[str, Engine] = {}

@app.get('/api/engines', response_model=PaginationResp[Engine])
async def get_engines():
    return {
        'items': [
            Engine(id='1', humanId=1, createdAt=1655476800, maxSpeedPm=100, nominalVoltage=120, nominalCurrent=10, weight=100),
            Engine(id='2', humanId=2, createdAt=1655476800, maxSpeedPm=100, nominalVoltage=120, nominalCurrent=10, weight=100),
            Engine(id='3', humanId=3, createdAt=1655476800, maxSpeedPm=100, nominalVoltage=120, nominalCurrent=10, weight=100)
        ],
        'cursor': 0,
        'page': 1,
        'pages': 1,
        'total': 3
    }

@app.post('/api/engines', response_model=Engine)
async def create_engine(engineData: Engine):
    return engineData

@app.get('/api/engines/{engineId}', response_model=Engine)
async def get_engine(engineId: str):
    return Engine(id=engineId, humanId=1, createdAt=1655476800, maxSpeedPm=100, nominalVoltage=120, nominalCurrent=10, weight=100)

@app.delete('/api/engines/{engineId}', status_code=204)
async def delete_engine(engineId: str):
    # remove from dict
    pass
