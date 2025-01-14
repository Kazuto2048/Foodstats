# imports from pip
from sqlalchemy import select

# imports from source code
from back.cfg import FoodDataAdd
from back.databese.db import new_session, FoodHistory


# class for DB functions
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