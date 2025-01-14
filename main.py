from back.funcs import readHistory, getProdByBarcode, getProdByName
from back.cfg import barcode, search_query


if __name__ == "__main__":
    readHistory()
    getProdByBarcode(barcode)
    getProdByName(search_query)