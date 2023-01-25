import asyncio
import websockets
import json

from binance import AsyncClient, BinanceSocketManager

from exchange.app.db import Currency


async def binance_exchange(cur_pair):  # BTCUSDT
    currency = cur_pair.split('-')
    pair_for_binance = str(currency[0] + currency[1])
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    sts = bm.symbol_ticker_socket(pair_for_binance)

    async with sts as tscm:
        res = await tscm.recv()
        res = float(res['w'])
        print(cur_pair, f"{res:0.1f}")
        # await Currency.objects.get_or_create(pair_name=cur_pair, price=f"{res:0.2f}")
    await client.close_connection()


async def okx_exchange(uri, channels_0):
    pair = channels_0[0]['instId']
    while True:
        try:
            async with websockets.connect(uri) as ws:
                sub_param = {"op": "subscribe", "args": channels_0}
                sub_str = json.dumps(sub_param)
                await ws.send(sub_str)
                while True:
                    res = await asyncio.wait_for(ws.recv(), timeout=100)
                    res = eval(res)
                    if 'event' not in res:
                        price_courses = res['data'][0][4]
                        print(pair, price_courses)
                        # await Currency.objects.get_or_create(pair_name=pair, price=price_courses)
                    else:
                        continue
                    await asyncio.sleep(5)
        except Exception as e:
            await binance_exchange(pair)
            continue

# channels = [{"channel": "mark-price", "instId": "ETH-USD-SWAP"}]  # ETH-USD-SWAP
# channels = [{"channel": "mark-price-candle1D", "instId": "BTC-USDT"}]
