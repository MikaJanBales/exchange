import uvicorn
import asyncio
from fastapi import FastAPI, WebSocket

from db import database, Currency
from exchange.exchange_ob import okx_exchange

app = FastAPI(title="Black Wall Group")


@app.get("/")
async def read_root():
    return await Currency.objects.all()


@app.websocket("/ws")
async def read_webscoket(websocket: WebSocket):
    await websocket.accept()
    currency_client = Currency()
    while True:
        data = await websocket.receive_json()
        currency = await currency_client.currency(data)
        await websocket.send_json(currency.dict())


@app.on_event("startup")
async def startup():
    channels = [{"channel": "mark-price-candle1D", "instId": "BTC-USDT"}]
    url = "wss://ws.okx.com:8443/ws/v5/public?brokerId=9999"
    if not database.is_connected:
        await database.connect()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(okx_exchange(url, channels))
    # loop.close()
    # okx_exchange(channels)
    await Currency.objects.get_or_create(pair_name='BTC-USDT', price=30000.01)


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)
