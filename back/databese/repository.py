# imports from pip
from datetime import datetime, timedelta
from sqlalchemy import select, update

# imports from source code
from back.cfg import FoodDataAdd, AddUserData
from back.databese.db import new_session, FoodHistory, Users


# class for history DB funcs
class HistoryRepository:
    # DB function to adding history
    @classmethod
    async def add_line(cls, historyLine: FoodDataAdd) -> int:
        # create a new session
        async with new_session() as session:
            historyLineDict = historyLine.model_dump()
            line = FoodHistory(**historyLineDict)
            session.add(line)
            # send req to DB and get id of line
            await session.flush()
            # commit changes
            await session.commit()
            return line.id

    # DB function to read history
    @classmethod
    async def get_all(cls):
        # create a new session
        async with new_session() as session:
            query = select(FoodHistory)
            # req to DB
            result = await session.execute(query)
            historyModels = result.scalars().all()
            return historyModels


# class for user DB funcs
class UsersRepository:
    # DB func for add user
    @classmethod
    async def add_user(cls, userData: AddUserData) -> int:
        async with new_session() as session:
            addUser = userData.model_dump()
            User = Users(**addUser)
            session.add(User)
            # send req to DB and get id of line
            await session.flush()
            # commit changes
            await session.commit()
            return User.id

    # DB func for login
    @classmethod
    async def login(cls, Username: str, Token: str):
        async with new_session() as session:
            time = datetime.now() + timedelta(hours=1)
            query = update(Users).where(Users.Username==Username).values(Token=Token, SessionEnd=time)
            res = await session.execute(query)
            return res

    # DB func for logout
    @classmethod
    async def logout(cls, Username: str):
        async with new_session() as session:
            query = update(Users).where(Users.Username == Username).values(Users.Token==None, SessionStart=None)
            await session.commit()

    # DB func to check username
    @classmethod
    async def isValidUsername(cls, Username: str) -> bool:
        async with new_session() as session:
            query = select(Users).where(Users.Username == Username)
            res = await session.execute(query)
            return res

    # DB func to get password
    @classmethod
    async def getPassword(cls, Username: str) -> bool:
        async with new_session() as session:
            query = select(Users.Password).where(Users.Username == Username)
            res = await session.execute(query)
            return res.scalar()

    # DB func to get token
    @classmethod
    async def getToken(cls, Username: str):
        async with new_session() as session:
            query = select(Users.Token).where(Users.Username == Username)
            res = await session.execute(query).scalar()
            return res

    # DB func to get session time
    @classmethod
    async def getSessionTime(cls, Username: str):
        async with new_session() as session:
            query = select(Users.SessionEnd).where(Users.Username == Username)
            res = await session.execute(query).scalar()
            return res