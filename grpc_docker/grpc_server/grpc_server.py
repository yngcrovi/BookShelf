import grpc
from concurrent import futures
from grpc_docker.grpc_server import book_pb2
from grpc_docker.grpc_server import book_pb2_grpc
import threading
from rabbitmq.consuming_message import rabbit_consumer
from fastapi_server.repository.service.book_service import book_service

class BookService(book_pb2_grpc.BookServicer):
    async def GetBook(self, request, context):
        book = await book_service.select_book({'id': request.id})
        if book:
            return book_pb2.GetBookResponse(
                id=book.id,
                name=book.name,
                author=book.author,
                date_of_publication=book.date_of_publication.strftime('%Y-%m-%d')
            )
        return book_pb2.GetBookResponse()

    async def GetAllBooks(self, request, context):
        books = await book_service.select_book()
        book_responses = []
        if type(books) == list:
            for i in range(len(books)):
                books[i] = books[i].model_dump()
                date_of_publication = books[i]['date_of_publication']
                book_responses.append(
                    book_pb2.GetBookResponse(
                        id=books[i]['id'],
                        name=books[i]['name'],
                        author=books[i]['author'],
                        date_of_publication=date_of_publication.strftime('%Y-%m-%d')
                    )
                )
        else:
            books = books.model_dump()
            date_of_publication = books['date_of_publication']
            book_responses.append(
                book_pb2.GetBookResponse(
                    id=books['id'],
                    name=books['name'],
                    author=books['author'],
                    date_of_publication=date_of_publication.strftime('%Y-%m-%d')
                )
            )
        return book_pb2.GetAllBooksResponse(books=book_responses)

async def grpc_server_run():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    book_pb2_grpc.add_BookServicer_to_server(BookService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("gRPC server started on port 50051")
    consumer_thread = threading.Thread(target=rabbit_consumer)
    consumer_thread.start()
    print("consumer listen...")
    await server.wait_for_termination()

