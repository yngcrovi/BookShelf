import pytest
from datetime import date
from contextlib import nullcontext as does_not_raise
from src.repository.service.book_service import book_service

current_data_for_insert = {
        "title": "Test Book",
        "author": "Test Author",
        "date_of_publication": date(2024, 1, 1) 
    }

not_current_data_for_insert = {
        "title": 2,
        "author": "Test Author",
        "date_of_publication": "2024-2-2"
    }


class TestBookAction:
    @pytest.mark.parametrize(
            "data, wait_res",
            [
                (current_data_for_insert, does_not_raise()),
                (not_current_data_for_insert, pytest.raises((AttributeError, AssertionError)))
            ]
    )
    @pytest.mark.asyncio
    async def test_add_book(self, data, wait_res):
        with wait_res:
            assert type(data['date_of_publication']) == date 
            data['date_of_publication'] = data['date_of_publication'].strftime('%Y-%m-%d')
            assert type(data) == dict
            assert type(data['date_of_publication']) == str
            assert type(data['title']) == str


    @pytest.mark.parametrize(
            "id_book, wait_res",
            [
                (1, pytest.raises(AssertionError)),
                (100, does_not_raise())
            ]
    )
    @pytest.mark.asyncio
    async def test_book_for_id(self, id_book, wait_res):
        with wait_res:
            book = await book_service.select_book({"id": id_book})
            assert type(book) == list
