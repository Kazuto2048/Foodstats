# imports from pip
from contextlib import asynccontextmanager

# imports from source code
from back.databese.db import drop_tables, create_tables
from back.routes import router as food_router
from fastapi import FastAPI


# function for startup and shut down
@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB request
    await drop_tables()
    print("БД очицена")
    # DB request
    await create_tables()
    print("БД создана")
    yield
    print("Выключаюсь...")


# construction for declaring API functions
app = FastAPI(lifespan=lifespan)
app.include_router(food_router)
