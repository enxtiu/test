from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    update: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class UserPoll(Base):
    __tablename__ = 'userpoll'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(3), nullable=False)
    descrip: Mapped[str] = mapped_column(String(350), nullable=False)

class UserData(Base):
    __tablename__ = 'userdata'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(nullable=False)
    clas: Mapped[str] = mapped_column(String(3), nullable=False)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)