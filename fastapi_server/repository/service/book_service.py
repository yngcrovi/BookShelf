from fastapi_server.repository.posgres.posgres import PostgreSQLRepository
from fastapi_server.repository.models.models import Book
from fastapi_server.repository.models.declarative_base.declarative_base import Base
from fastapi_server.repository.service.dto_form.dto_form import GetIdBookDTO


class BookService(PostgreSQLRepository):

    def __init__(self, table: Base):
        self.table = table

    async def select_book(self, filter_data: dict = None, dto = GetIdBookDTO) -> GetIdBookDTO:
        result = await self.select_data(filter_data)
        res = result.scalars().all()
        result_dto = self.get_dto_form(dto, res)
        return result_dto
    

    async def insert_book(self, data: dict) -> Book:
        value = await self.insert_data(data)
        return value

    async def update_book(self, upd_id: int, upd_data: dict):
        await self.update_data(upd_id, upd_data)

    async def delete_book(self, id: int):
        await self.delete_data(id)

book_service = BookService(Book)