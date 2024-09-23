from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from grpc_service.grpc_client import GrpcClient
from grpc_service import book_pb2_grpc, book_pb2
from auth_user.check_auth import check_auth

route = APIRouter(
    prefix='/grpc-book',
    tags=['gRPC book actions'],
    dependencies=[Depends(check_auth)]
)

@route.get("/all")
@cache(expire=20)
async def get_all_books() -> JSONResponse:
    async with GrpcClient('localhost:50051') as channel:
        stub = book_pb2_grpc.BookStub(channel)
        request = book_pb2.GetAllBooksRequest()
        response = await stub.GetAllBooks(request)
        books_list = []
        print(response)
        for book in response.books:
            book_dict = {
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'date_of_publication': book.date_of_publication
            }
            books_list.append(book_dict)
        if books_list:
            return JSONResponse(
                content=books_list,
                status_code=200
            )
        error = {"error": "The bookshelf is empty"}
        return JSONResponse(
            content=error,
            status_code=404
        )

@route.get("/{book_id}")
@cache(expire=20)
async def get_book_for_id(book_id: int) -> JSONResponse:
    async with GrpcClient('localhost:50051') as channel:
        stub = book_pb2_grpc.BookStub(channel)
        request = book_pb2.GetBookRequest(id=book_id)
        response = await stub.GetBook(request)
        if response:
            book = {
                "id": response.id,
                "name": response.name,
                "author": response.author,
                "date_of_publication": response.date_of_publication
            }
        if book["id"] != 0:
            return JSONResponse(    
                content=book,
                status_code=200
            )
        error = {"error": "Book not found"}
        return JSONResponse(
            content=error,
            status_code=404
        )
    