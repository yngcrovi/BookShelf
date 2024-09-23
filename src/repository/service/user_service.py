from repository.posgres.posgres import PostgreSQLRepository
from repository.models.models import User
from repository.models.declarative_base.declarative_base import Base
from repository.service.dto_form.dto_form import GetUserDTO, GetUserSaltDTO


class UserService(PostgreSQLRepository):

    def __init__(self, table: Base):
        self.table = table

    async def select_user(self, filter_data: dict) -> GetUserDTO:
        result = await self.select_data(filter_data)
        res = result.scalars().all()
        result_dto = self.get_dto_form(GetUserDTO, res)
        return result_dto
       
    async def select_user_salt(self, filter_data: dict, dto = GetUserSaltDTO) -> GetUserSaltDTO:
        result = await self.select_data(filter_data)
        res = result.scalars().all()
        result_dto = self.get_dto_form(dto, res)
        return result_dto
    
    async def insert_user(self, data: dict) -> User:
        value = await self.insert_data(data)
        return value

user_service = UserService(User)