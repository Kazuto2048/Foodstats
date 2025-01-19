# imports from pip
from datetime import datetime
import secrets
import bcrypt
import requests
from typing import Annotated
from fastapi.params import Depends

# imports from source code
from back.cfg import FoodDataAdd, RequestData, AddUserData, UserLogin, checkSession
from back.databese.repository import HistoryRepository, UsersRepository


# func for read history from DB
async def readHistory(session: Annotated[checkSession, Depends()]):
    if await checkToken(session.Username, session.Token):
        # DB request
        res = await HistoryRepository.get_all()
        print(res)
        # check is there any hictory
        if res != []:
                return res
        else:
            return "Истории еще нет"
    else:
        return "invalid token"

# func for write new line in history DB
async def writeHistory(prod: Annotated[FoodDataAdd, Depends()], session: Annotated[checkSession, Depends()]) -> str:
    if await checkToken(session.Username, session.Token):
        # DB request
        return await HistoryRepository.add_line(prod)
    else:
        return "invalid token"

# func for delete history DB
async def deleteHistory(session: Annotated[checkSession, Depends()]):
    if await checkToken(session.Username, session.Token):
        # DB requests
        await HistoryRepository.deleteHistory()
        return "История успешно удалена"
    else:
        return "invalid token"

# func for get data of product by api (for request needs a barcode)
async def getProdByBarcode(reqData: RequestData):

    url = f"https://ru.openfoodfacts.org/api/v0/product/{reqData.Data}.json"

    response = requests.get(url)
    #request processing
    if response.status_code == 200:
        data = response.json()
        # if there is data on the request in the response
        if data.get("status") == 1:
            product = data.get("product", {})
            # extract name from query data
            product_name = product.get("product_name_ru", product.get("product_name", "Нет названия"))
            # extract calories from query data
            energy_kcal = product.get("nutriments", {}).get("energy-kcal", "Нет данных")
            # extract weight/volume from query data
            quantity = product.get("quantity", "Нет данных")
            return [product_name, energy_kcal, quantity, reqData.UserId]
        # if there isn`t ane data on the request in the response
        else:
            return "Продукт не найден."
    # error handling
    else:
        return f"Ошибка запроса: {response.status_code}"

# func for getting data of product by api (for request needs a name)
async def getProdByName(search_query: str):
    prods = []
    url = f"https://ru.openfoodfacts.org/cgi/search.pl?search_terms={search_query}&search_simple=1&action=process&json=1"

    response = requests.get(url)
    # request processing
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])
        # if there is data on the request in the response
        if products:
            print(f"Найдено продуктов: {len(products)}")
            for product in products:
                # extract name from query data
                product_name = product.get("product_name", "Нет названия").replace("&quot;", "\"")
                # extract calories from query data
                energy_kcal = product.get("nutriments", {}).get("energy-kcal", "Нет данных")
                # extract weight/volume from query data
                quantity = product.get("quantity", "Нет данных")
                # append product_name, energy_kcal, quantity to the list
                prods.append(f"- {product_name} (Энергетическая ценность: {energy_kcal} ккал, объем/вес: {quantity})")
                return prods
        # if there isn`t data on the request in the response
        else:
            return "Продукты не найдены."
    # error handling
    else:
        return f"Ошибка запроса: {response.status_code}"

# func for check free usernames
async def getValidUsername(Username: str) -> bool:
    # DB request
    res = await UsersRepository.isValidUsername(Username)
    return res

# func for add user
async def addUserToDB(User: Annotated[AddUserData, Depends()]) -> int:
    User.Password = await generateHash(User.Password)
    # DB request
    return await UsersRepository.add_user(User)

# func for login
async def userLogin(User: Annotated[UserLogin, Depends()]) -> str:
    # DB requests
    username = await UsersRepository.isValidUsername(User.Username)
    password = await checkPassword(User.Password, User.Username)
    if username and password:
        # generate token
        token = secrets.token_hex(32)
        # BD request
        await UsersRepository.login(User.Username, token)
        return str(token)
    else:
        return "Неверный логин или пароль"

# func for check token
async def checkToken(Username: str, Token: str) -> bool:
    # DB request
    token = await UsersRepository.getToken(Username)
    SessionEnd = await UsersRepository.getSessionTime(Username)
    if token == Token:
        if datetime.now() < SessionEnd:
            return True
        else:
            await UsersRepository.logout(Username)
            return False
    else:
        return False

# func for generate hash
async def generateHash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode()

#func for check password
async def checkPassword(password: str, Username: str) -> bool:
    passwordHash = await UsersRepository.getPassword(Username)
    if passwordHash != None:
        return bcrypt.checkpw(password.encode('utf-8'), passwordHash.encode('utf-8'))
    else:
        return False