import uvicorn
import asyncio
from fastapi import FastAPI

from db import database, Currency
from exchange.exchange_ob import okx_exchange

app = FastAPI(title="Black Wall Group")


def get_exchange(pair_name: str):  # example: BTC-USDT
    channel = [{"channel": "mark-price-candle1D", "instId": pair_name}]
    url = "wss://ws.okx.com:8443/ws/v5/public?brokerId=9999"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(okx_exchange(url, channel))
    loop.close()


@app.get("/")
async def read_root():
    return await Currency.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    await Currency.objects.get_or_create(pair_name='BTC-USDT', price=30000.01)


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

get_exchange('BTC-USDT')

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)
