import time
import hmac
import hashlib
import requests
import urllib.parse

class BinanceFutures:
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = bytearray(API_SECRET, encoding='utf-8')
        self.shift_seconds = 0

        self.methods = {
            'exchangeInfo': {'url': 'fapi/v1/exchangeInfo', 'method': 'GET', 'private': False},
            'futures_symbol_ticker': {'url': 'fapi/v1/ticker/price', 'method': 'GET', 'private': False},
            'futures_account': {'url': 'fapi/v2/account', 'method': 'GET', 'private': True},
            'futures_create_order': {'url': 'fapi/v1/order', 'method': 'POST', 'private': True},
            'futures_cancel_order': {'url': 'fapi/v1/order', 'method': 'DELETE', 'private': True},
            'futures_order_info': {'url': 'fapi/v1/order', 'method': 'GET', 'private': True},
            'futures_open_orders': {'url': 'fapi/v1/openOrders', 'method': 'GET', 'private': True},
            'futures_my_trades': {'url': 'fapi/v1/userTrades', 'method': 'GET', 'private': True}
        }
    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            kwargs.update({'command': name})
            return self.call_api(**kwargs)
        return wrapper

    def set_shift_seconds(self, seconds):
        self.shift_seconds = seconds
        
    def get_symbol_info(self, symbol):
        info = self.call_api(command='exchangeInfo')
        for s in info['symbols']:
            if s['symbol'] == symbol:
                for f in s['filters']:
                    if f['filterType'] == 'LOT_SIZE':
                        return {
                            'quantity_step': f['stepSize']
                        }
        raise ValueError(f"Symbol info for {symbol} not found")    

    def call_api(self, **kwargs):
        command = kwargs.pop('command')
        method_conf = self.methods[command]
        base_url = 'https://fapi.binance.com/'
        api_url = base_url + method_conf['url']

        payload = kwargs
        headers = {}
        payload_str = urllib.parse.urlencode(payload)

        if method_conf['private']:
            payload.update({
                'timestamp': int(time.time() + self.shift_seconds - 1) * 1000,
                'recvWindow': 10000
            })
            payload_str = urllib.parse.urlencode(payload).encode('utf-8')
            sign = hmac.new(
                key=self.API_SECRET,
                msg=payload_str,
                digestmod=hashlib.sha256
            ).hexdigest()
            payload_str = payload_str.decode("utf-8") + "&signature=" + str(sign)
            headers = {"X-MBX-APIKEY": self.API_KEY}

        if method_conf['method'] == 'GET':
            api_url += '?' + payload_str
            response = requests.get(api_url, headers=headers)
        else:
            response = requests.request(    
            method=method_conf['method'],
                url=api_url,
                data=payload_str,
                headers=headers
            )

        if 'code' in response.text:
            print(response.text)
        return response.json()