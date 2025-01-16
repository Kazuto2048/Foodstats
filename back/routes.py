# imports from pip
from typing import Annotated
from fastapi.params import Depends
from fastapi import APIRouter

# imports from source code
from back.cfg import FoodDataAdd, RequestData, AddUserData, UserLogin, checkSession
from back.funcs import getProdByName, getProdByBarcode, deleteHistory, writeHistory, readHistory, getValidUsername, addUserToDB, userLogin

# construction for declaring API functions
router = APIRouter(prefix="/api")


# API function for processing barcode data req
@router.get("/barcode")
async def getDataByBarcode(reqData: Annotated[RequestData, Depends()]):
    return await getProdByBarcode(reqData)

# API function for processing name data req
@router.get("/name")
async def getDataByName(reqData: Annotated[RequestData, Depends()]):
    return await getProdByName(reqData)

# API function for processing read history req
@router.get("/history/read")
async def readHistoryData(session: Annotated[checkSession, Depends()]):
    return await readHistory(session)

# API function for processing write history req
@router.post("/history/write")
async def writeHistoryData(food: Annotated[FoodDataAdd, Depends()], session: Annotated[checkSession, Depends()]):
    return await writeHistory(food, session)

# API function for processing delete history req
@router.get("/history/delete")
async def deleteHistoryData(session: Annotated[checkSession, Depends()]):
    return await deleteHistory(session)

# API func for add user
@router.get("/addUser")
async def addUser(User: Annotated[AddUserData, Depends()]):
    if await getValidUsername(User.Username):
        return {"Status": 200, "id": await addUserToDB(User)}
    else:
        return "Такой Юзернейм уже существует"

# API func for login
@router.post("/login")
async def login(User: Annotated[UserLogin, Depends()]):
    return await userLogin(User)
