from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from repository.service.user_service import user_service
from auth_user.token import get_access_token
from auth_user.hash_password import make_hesh_password, compare_hesh_password

route = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

class UserRegistration(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

async def user_exists_for_registration(user: UserRegistration):
    username = {'username': user.username}
    check_exist = await user_service.select_user(username)
    if check_exist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User exists",
        )
    else: 
        return user.model_dump()
    
async def user_exists_for_login(user: UserLogin) -> UserLogin:
    username = {'username': user.username}
    check_exist = await user_service.select_user(username)
    if check_exist:
        user = user.model_dump()
        user['hash_password'] = check_exist.hash_password
        user['id'] = check_exist.id
        return user
    else: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not exists",
        )


@route.post("/registration")
async def registration(
    user_data: Annotated[dict, Depends(user_exists_for_registration)],
    access_token: str = Cookie(default=None)
) -> JSONResponse:
    if access_token:
        error = {
            "error": "Registration cannot be completed while you are logged in!"
        }
        return JSONResponse(
            content=error,
            status_code=401
        )
    key_salt = make_hesh_password(user_data['password'])
    user_data.update(key_salt)
    del user_data['password']
    id_username = await user_service.insert_user(user_data)
    user_data['id'] = id_username.id
    access_token = get_access_token(user_data)
    info = {"info": "Registration was successful"}
    response = JSONResponse(
        content=info,
        status_code=200
    )
    response.set_cookie(key='access_token', value=f'{access_token}', httponly=True)
    return response

@route.post("/login")
async def login(
    user_data: Annotated[dict, Depends(user_exists_for_login)],
    access_token: str = Cookie(default=None)
) -> JSONResponse:
    if access_token:
        error = {
            "error": "You are already logged in!"
        }
        return JSONResponse(
            content=error,
            status_code=401
        )
    user_salt = await user_service.select_user_salt({'id': user_data['id']})
    if not compare_hesh_password(user_data['password'], user_salt.salt, user_data['hash_password']):
        error = {
            'Error': 'Incorrect password'
        }
        return JSONResponse(
            content=error, 
            status_code = 401
            )
    access_token = get_access_token(user_data)
    info = {
        "info": "Login successful"
    }
    response = JSONResponse(
        content=info, 
        status_code=200
        )
    response.set_cookie(key='access_token', value=f'{access_token}', httponly=True, domain='127.0.0.1')
    return response

@route.post("/logout")
async def logout(
    access_token: str = Cookie(default=None)
) -> JSONResponse:
    if not access_token:
        error = {
            "error": "Account login failed!"
        }
        return JSONResponse(
            content=error,
            status_code=401
        )
    info = {
        "info": "Logout successful"
    }
    response = JSONResponse(
        content=info, 
        status_code=200
        )
    response.delete_cookie(key='access_token', httponly=True, domain='127.0.0.1')
    return response