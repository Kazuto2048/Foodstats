from back.routes import router as food_router
from fastapi import FastAPI


app = FastAPI()
app.include_router(food_router)
