# imports from pip
from sqlalchemy import select
from sqlalchemy.util import await_only

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
    async def login(cls, Username: str):
        pass

    # DB func for logoff

    # DB func for logout
    @classmethod
    async def logout(cls):
        pass

    # DB func for get all usernames
    @classmethod
    async def isValidUsername(cls, username: str) -> bool:
        async with new_session() as session:
            query = select(Users).where(Users.Username == username)
            res = await session.execute(query)
            return res is not None