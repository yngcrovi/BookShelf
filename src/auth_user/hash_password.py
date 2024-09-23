import os
import hashlib

def make_hesh_password(password: str) -> dict:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', f'{password}'.encode('utf-8'), salt, 100000)
    return {'hash_password': key, 'salt': salt}

def compare_hesh_password(password: str, salt: bytes, compare_password: str) -> bool: 
    key = hashlib.pbkdf2_hmac('sha256', f'{password}'.encode('utf-8'), salt, 100000)
    if key == compare_password:
        return True
    else: 
        return False