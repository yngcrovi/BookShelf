import pytest
from contextlib import nullcontext as does_not_raise
from src.auth_user.hash_password import make_hesh_password, compare_hesh_password


class TestAuth:
    @pytest.mark.parametrize(
        "password, compare_password, wait_res",
        [
            ('test', 'test', does_not_raise()),
            ('test', 'test1', pytest.raises(AssertionError))
        ]
    )
    @pytest.mark.asyncio
    async def test_add_book(self, password, compare_password, wait_res):
        with wait_res:
            key_salt = make_hesh_password(password)
            assert compare_hesh_password(compare_password, key_salt['salt'], key_salt['hash_password']) == True