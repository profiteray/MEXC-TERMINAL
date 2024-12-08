import requests
import hmac
import hashlib
import time
import urllib.parse

# MEXC API Bilgileri
API_KEY = "access key bilginizi girin"
API_SECRET = " secret bilginizi girin"
BASE_URL = "https://api.mexc.com/api/v3"


def create_signature(params):
    query_string = urllib.parse.urlencode(params)
    return hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()



def get_usdt_balance():
    url = f"{BASE_URL}/account"
    headers = {"X-MEXC-APIKEY": API_KEY}
    params = {"timestamp": int(time.time() * 1000)}
    params["signature"] = create_signature(params)
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Bakiyeniz alınamadı: {response.json()}")
        return 0.0

    try:
        balances = response.json().get("balances", [])
        usdt_balance = next((float(asset["free"]) for asset in balances if asset["asset"] == "USDT"), 0.0)
        return usdt_balance
    except Exception as e:
        print(f"USDT bakiyesi alınırken hata oluştu: {e}")
        return 0.0


def get_asset_balance(asset):
    url = f"{BASE_URL}/account"
    headers = {"X-MEXC-APIKEY": API_KEY}
    params = {"timestamp": int(time.time() * 1000)}
    params["signature"] = create_signature(params)

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Bakiye alınamadı: {response.json()}")
        return 0.0

    try:
        balances = response.json().get("balances", [])
        asset_balance = next((float(asset_info["free"]) for asset_info in balances if asset_info["asset"] == asset),
                             0.0)
        return asset_balance
    except Exception as e:
        print(f"{asset} bakiyesi alınırken hata oluştu: {e}")
        return 0.0


def is_valid_symbol(symbol):
    url = f"{BASE_URL}/exchangeInfo"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Exchange bilgileri alınamadı: {response.json()}")
        return False

    try:
        symbols_info = response.json().get("symbols", [])
        for symbol_info in symbols_info:
            if symbol_info["symbol"] == symbol:
                # Boş filters listesi olsa bile sembolü geçerli say
                return symbol_info
        return None
    except Exception as e:
        print(f"Sembol bilgileriişlenirken hata: {e}")
        return None


def market_order(symbol, side, usdt_amount=None, quantity=None):
    url = f"{BASE_URL}/order"
    headers = {"X-MEXC-APIKEY": API_KEY}

    symbol_info = is_valid_symbol(symbol)
    if not symbol_info:
        print(f"Sembol geçersiz: {symbol}. Lütfen doğru sembolü girin.")
        return

    if side.upper() == "SELL" and quantity is None:
        base_asset = symbol.replace("USDT", "")
        quantity = get_asset_balance(base_asset)

        if quantity == 0:
            print(f"Satılacak {base_asset} bakiyesi yok.")
            return

    price_url = f"{BASE_URL}/ticker/price?symbol={symbol}"
    response = requests.get(price_url)
    if response.status_code != 200:
        print(f"Fiyat alınamadı: {response.json()}")
        return

    price = float(response.json().get("price", 0))
    if price == 0:
        print("Fiyat sıfır, işlem yapılamaz.")
        return

    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "MARKET",
        "timestamp": int(time.time() * 1000),
    }

    if quantity is not None:
        params["quantity"] = quantity
    elif usdt_amount is not None:
        params["quoteOrderQty"] = usdt_amount

    params["signature"] = create_signature(params)
    response = requests.post(url, headers=headers, params=params)
    result = response.json()

    if "code" in result and result["code"] != 0:
        print(f"İşlem başarısız: {result.get('msg', 'Bilinmeyen hata')}")
    else:
        print(f"İşlem başarılı: {result}")


print("MEXC Trading Terminal")
usdt_balance = get_usdt_balance()
print(f"Mevcut USDT bakiyeniz: {usdt_balance:.2f} USDT")

while True:
    komut = input("Komut girin (örnek: wojak 10 buy veya wojak sell): ").strip().lower()
    if not komut:
        print("Çıkış yapılıyor.")
        break

    try:
        args = komut.split()
        symbol = args[0].upper() + "USDT"

        if len(args) == 1 or args[1] == "sell":
            # Tüm bakiyeyi sat
            market_order(symbol, "SELL")
        elif args[1] == "buy":
            # USDT miktarını al
            usdt_amount = float(args[2].replace("k", "000"))
            market_order(symbol, "BUY", usdt_amount=usdt_amount)
        else:
            # Miktar belirtilmişse
            amount = float(args[1].replace("k", "000"))
            side = "SELL" if "sell" in komut else "BUY"
            market_order(symbol, side, usdt_amount=amount)

        usdt_balance = get_usdt_balance()
        print(f"Mevcut USDT bakiyeniz: {usdt_balance:.2f} USDT")
    except Exception as e:
        print(f"Hata: {e}")
