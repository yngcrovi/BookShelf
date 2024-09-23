from fastapi import Cookie, HTTPException, status

def check_auth(access_token: str = Cookie(default=None)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Register or log in to your account!",
        )