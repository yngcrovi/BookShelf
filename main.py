from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_server.endpoint_book.book_actions import route as book_actions
from fastapi_server.endpoint_book.grpc_book_actions import route as grpc_book_actions
from fastapi_server.auth_user.endpoint_auth.endpoint_auth import route as auth

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis))

app.include_router(book_actions)
app.include_router(grpc_book_actions)      
app.include_router(auth)   