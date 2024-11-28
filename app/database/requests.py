from app.database.models import async_session
from app.database.models import User, City, User_City
from sqlalchemy import select, and_

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def set_city(city_name):
    async with async_session() as session:
        city = await session.scalar(select(City).where(City.name == city_name))

        if not city:
            session.add(City(name=city_name))
            await session.commit()

async def set_pair(tg_id, city_name):
    async with async_session() as session:
        pair = await session.scalar(select(User_City).join(User, User_City.user_id == User.id).
                                    join(City, User_City.city_id == City.id).
                                    where(and_(User.tg_id == tg_id, City.name == city_name)))

        if not pair:
            session.add(User_City(city_id= await session.scalar(select(City.id).where(City.name == city_name)),
                                  user_id= await session.scalar(select(User.id).where(User.tg_id == tg_id))))
            await session.commit()

async def get_cities(tg_id):
    async with async_session() as session:
        result =  await session.scalars(select(City).join(User_City, City.id == User_City.city_id).
                                     join(User, User_City.user_id == User.id).
                                     where(User.tg_id == tg_id))

        return result.all()

async def check(tg_id):
    async with async_session() as session:
        result =  await session.scalars(select(City).join(User_City, City.id == User_City.city_id).
                                     join(User, User_City.user_id == User.id).
                                     where(User.tg_id == tg_id))

        return len(result.all()) == 0

