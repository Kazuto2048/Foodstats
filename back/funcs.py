# imports from pip
import requests
from typing import Annotated
from fastapi.params import Depends

# imports from source code
from back.cfg import FoodDataAdd, RequestData
from back.databese.db import drop_tables, create_tables
from back.databese.repository import HistoryRepository


# func for read history from DB
async def readHistory():
    # DB request
    res = await HistoryRepository.get_all()
    print(res)
    # check is there any hictory
    if res != []:
            return res
    else:
        return "Истории еще нет"

# func for write new line in history DB
async def writeHistory(prod:  Annotated[FoodDataAdd, Depends()]):
    # DB request
    return await HistoryRepository.add_line(prod)

# func for delete history DB
async def deleteHistory():
    # DB requests
    await drop_tables()
    await create_tables()
    return "История успешно удалена"

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
