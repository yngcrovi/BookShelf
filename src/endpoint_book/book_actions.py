from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
import datetime
from repository.service.book_service import book_service
from rebbitmq.publish_message import publish_message
from auth_user.check_auth import check_auth

route = APIRouter(
    prefix='/book',
    tags=['FastAPI book actions'],
    dependencies=[Depends(check_auth)]
)

class NewBook(BaseModel):
    name: str
    author: str
    date_of_publication: datetime.date

class EditBook(BaseModel):
    name: str
    author: str
    date_of_publication: datetime.date


@route.post('/add')
async def add_book(
    new_book: NewBook
) -> JSONResponse:
    new_book = new_book.model_dump()
    new_book['date_of_publication'] = new_book['date_of_publication'].strftime('%Y-%m-%d')
    await book_service.insert_book(new_book)
    publish_message("add_book", {'new_book': new_book})
    info = {
        "info": "The book has been added successfully"
    }
    return JSONResponse(
        content=info,
        status_code=200
    )

@route.get("/all")
@cache(expire=20)
async def get_books() -> JSONResponse:
    books = await book_service.select_book()
    if books:
        list_books = []
        if type(books) == list:
            for i in range(len(books)):
                books[i] = books[i].model_dump()
                books[i]['date_of_publication'] = books[i]['date_of_publication'].strftime('%Y-%m-%d')
                list_books.append(books[i])
        else:
            books = books.model_dump()
            books['date_of_publication'] = books['date_of_publication'].strftime('%Y-%m-%d')
            list_books.append(books)
        publish_message("get_all_book", {'list_books': list_books})
        return JSONResponse(
            content=list_books,
            status_code=200
        )
    error = {
        "error": "Book not found"
    }
    return JSONResponse(
        content=error,
        status_code=404
    )

@route.get("/{id_book}")
@cache(expire=20)
async def get_book_for_id(id_book: int) -> JSONResponse:
    book = await book_service.select_book({'id': id_book})
    if book:
        book = book.model_dump()
        book['date_of_publication'] = book['date_of_publication'].strftime('%Y-%m-%d')
        publish_message("get_book_for_id", id_book)
        return JSONResponse(
            content=book,
            status_code=200
        )
    error = {
        "error": "Book not found"
    }
    return JSONResponse(
        content=error,
        status_code=404
    )

@route.put("/edit/{id_book}")
async def edit_book(id_book: int, edit_data: EditBook) -> JSONResponse:
    book = await book_service.select_book({'id': id_book})
    if not book:
        error = {
            "error": "Book not found"
        }
        return JSONResponse(
            content=error,
            status_code=404
        )
    edit_data = edit_data.model_dump()
    edit_data['date_of_publication'] = edit_data['date_of_publication'].strftime('%Y-%m-%d')
    await book_service.update_book(id_book, edit_data)
    info = {"Info": "The book has been updated successfully"}
    publish_message("update_book", {'id': id_book, **edit_data})
    return JSONResponse(
        content=info,
        status_code=200
    )


@route.delete("/drop/{id_book}")
async def drop_book(id_book: int) -> JSONResponse:
    book = await book_service.select_book({'id': id_book})
    if not book:
        error = {"error": "Book not found"}
        return JSONResponse(
            content=error,
            status_code=404
        )
    await book_service.delete_book(id_book)
    info = {"Info": "The book has been delete successfully"}
    publish_message("delete_book", {'id': id_book})
    return JSONResponse(
        content=info,
        status_code=200
    )
