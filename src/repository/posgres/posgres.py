from repository.config.engine import async_session_factory
from sqlalchemy import select, update, delete
from repository.models.declarative_base.declarative_base import Base
from pydantic import BaseModel
from .abc import AbstractRepository

class PostgreSQLRepository(AbstractRepository):
    asf = async_session_factory
    table = Base

    #поменять ABC класс под текущие функции
    async def insert_data(self, insert_data: dict):
        async with self.asf() as session:
            rows_to_insert = self.table(**insert_data)
            session.add(rows_to_insert)
            await session.flush()
            await session.refresh(rows_to_insert)
            await session.commit()
            return rows_to_insert

    async def select_data(self, filter_data: dict | None):
        async with self.asf() as session:
            if type(filter_data) is dict:
                query = (
                    select(self.table)
                    .filter_by(**filter_data)
                )
            else:
                query = (
                    select(self.table)
                    .order_by(self.table.id)
                )
            result = await session.execute(query)
            return result
        
    async def delete_data(self, id: int):
        async with self.asf() as session:
            query = (
                delete(self.table)
                .filter(self.table.id == id)
            )
            await session.execute(query)
            await session.commit()
        
    async def update_data(self, upd_id: int, upd_data: dict) -> None:
        async with self.asf() as session:
            upd = (
                update(self.table)
                .filter(self.table.id == upd_id)
                .values(upd_data)
            )
            await session.execute(upd)
            await session.commit()

    def get_dto_form(self, dto_form: BaseModel, res: list):
        result_dto = [dto_form.model_validate(row, from_attributes=True) for row in res]
        if len(result_dto) == 1:
            result_dto = result_dto[0]
        return result_dto