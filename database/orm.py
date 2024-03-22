from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import types

from database.model import UserPoll, UserData

async def add_userpoll(session: AsyncSession, data: dict):
    obj = UserPoll(
        number=data['number'],
        descrip=data['descrip']
    )
    session.add(obj)
    await session.commit()

async def add_userdata(session: AsyncSession, data: dict):
    obj = UserData(
        userid=data['id'],
        clas=data['clas'],
        login=data['login'],
        password=data['password']
    )
    session.add(obj)
    await session.commit()