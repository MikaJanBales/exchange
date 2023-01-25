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
        # while True:
        res = await tscm.recv()
        res = float(res['w'])
        # print(f"{res:0.2f}")
        await [cur_pair, float(f"{res:0.2f}")]
        await asyncio.sleep(4)
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
                        await [pair, price_courses]
                    else:
                        continue
                    await asyncio.sleep(4)
        except Exception as e:
            await binance_exchange(pair)
            continue


# url = "wss://ws.okx.com:8443/ws/v5/public?brokerId=9999"

# channels = [{"channel": "tickers", "instId": "EUR-USD-SWAP"}]
# channels = [{"channel": "candle1m", "instId": "USDT-EUR"}]
# channels = [{"channel": "trades", "instId": "USDT-EUR"}]
# channels = [{"channel": "mark-price", "instId": "ETH-USD-SWAP"}]  # ETH-USD-SWAP
# channels = [{"channel": "mark-price-candle1D", "instId": "BTC-USDT"}]
# channels = [{"channel": "price-limit", "instId": "USDT-EUR-SWAP"}]
# channels = [{"channel": "index-candle1m", "instId": "USDT-EUR"}]
# channels = [{"channel": "index-tickers", "instId": "USDT-EUR"}]


# loop = asyncio.get_event_loop()
#
# loop.run_until_complete(okx_exchange(url, channels))
#
# loop.close()

# api_key = "a4918bd9-5733-4057-b76d-bb28c9ba2e1d"
# secret_key = "48A80F86B5647D92973223B562621100"
# passphrase = "FGmXGP43tcdGpCj_"
