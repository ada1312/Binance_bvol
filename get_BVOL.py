import websocket
import ssl
import json
import time
import schedule
import threading

SOCKET = 'wss://fstream.binance.com/stream'

paramsETH = {
    "method": "SUBSCRIBE",
    "params": [
        "iETHBVOLUSDT@kline_30m",
    ],
    "id": 4
}

paramsBTC = {
    "method": "SUBSCRIBE",
    "params": [
        "iBTCBVOLUSDT@kline_30m",
    ],
    "id": 6
}

def subscribe(ws, params):
    ws.send(json.dumps(params))

def on_open(ws):
    subscribe(ws, paramsETH)
    subscribe(ws, paramsBTC)

def on_close(ws):
    print('Closed Connection')

def on_message(ws, message):
    try:
        data = json.loads(message)
        if 'k' in data['data'] and 'c' in data['data']['k']:
            symbol = data['data']['s']
            close_price = data['data']['k']['c']
            print(f"{symbol}: {close_price}")
    except Exception as e:
        print(f"Error processing message: {e}")

def on_error(ws, err):
    print("Got an error: ", err)


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

