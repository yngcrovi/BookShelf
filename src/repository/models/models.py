from sqlalchemy.orm import Mapped, mapped_column
from .declarative_base.declarative_base import Base
import datetime
 

class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    date_of_publication: Mapped[datetime.date] = mapped_column(nullable=False)

    repr_cols_num = 3

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hash_password: Mapped[bytes] = mapped_column(nullable=False)
    salt: Mapped[bytes]

    repr_cols_num = 3