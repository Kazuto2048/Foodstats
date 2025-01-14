import codecs
import requests
from datetime import datetime
import os

# func for read history from file
def readHistory():
    if os.path.getsize("history.txt") != 0:
        with codecs.open("history.txt", "r", "UTF-8") as f:
            history = f.read()
            return history
    else:
        return "Истории еще нет"

# func for write new line in history file
def writeHistory(prod: str):
    with codecs.open("history.txt", "a", "UTF-8") as f:
        if os.path.getsize("history.txt") != 0:
            f.write(f"\n{prod}")
        else:
            f.write(prod)
            print(f"Система: Продукт \"{prod}\" успешно добавлен в историю; Дата: {datetime.now().strftime('%Y-%m-%d')}; Время: {datetime.now().strftime('%H:%M:%S')}")

# func for delete history
def deleteHistory():
    with codecs.open("history.txt", "r", "UTF-8") as f:
        f.truncate(0)

# func for get data of product by api (for request needs a barcode)
def getProdByBarcode(barcode: str):
    url = f"https://ru.openfoodfacts.org/api/v0/product/{barcode}.json"

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
            return f"- {product_name} (Энергетическая ценность: {energy_kcal} ккал, объем/вес: {quantity})"
        # if there isn`t ane data on the request in the response
        else:
            return "Продукт не найден."
    # error handling
    else:
        return f"Ошибка запроса: {response.status_code}"

# func for getting data of product by api (for request needs a name)
def getProdByName(search_query: str):
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