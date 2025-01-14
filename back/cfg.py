# imports from pip
from pydantic import BaseModel

# class for API and funcs usage
class RequestData(BaseModel):
    Data: str
    UserId: int

# class for API and funcs usage
class FoodDataAdd(BaseModel):
    Name: str
    Kcal: int
    Quantity: str
    UserId: int

# class for DB usage
class FoodData(FoodDataAdd):
    id: int


# temporary variables
barcode = "4650075427736"
search_query = "Шоколад молочный милка"

#main variables
pass

# database variables
host = None
database = None
user = None
password = None
port = None
