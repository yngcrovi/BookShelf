from abc import ABC, abstractclassmethod

class AbstractRepository(ABC):
    @abstractclassmethod
    async def insert_data():
        raise NotImplementedError
    
    @abstractclassmethod
    async def select_data():
        raise NotImplementedError
    
    @abstractclassmethod
    async def delete_data():
        raise NotImplementedError
    
    @abstractclassmethod
    async def update_data():
        raise NotImplementedError

    