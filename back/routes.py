from back.funcs import getProdByName, getProdByBarcode, deleteHistory, writeHistory, readHistory
from fastapi import APIRouter


router = APIRouter()


@router.get("/barcode")
def getDataByBarcode(barcode: str):
    return getProdByBarcode(barcode)

@router.get("/name")
def getDataByName(name: str):
    return getProdByName(name)

@router.get("/history/read")
def readHistoryData():
    return readHistory()

@router.get("/history/write")
def writeHistoryData(product: str):
    return writeHistory(product)

@router.get("/history/delete")
def deleteHistoryData():
    return deleteHistory()
