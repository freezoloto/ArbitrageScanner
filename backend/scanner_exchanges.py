import ccxt

# Реальные комиссии бирж (в процентах)
FEES = {
    "binance":     {"maker": 0.1,  "taker": 0.1},
    "bybit":       {"maker": 0.1,  "taker": 0.1},
    "okx":         {"maker": 0.08, "taker": 0.1},
    "kucoin":      {"maker": 0.1,  "taker": 0.1},
    "gate":        {"maker": 0.2,  "taker": 0.2},
    "mexc":        {"maker": 0.0,  "taker": 0.2},
    "bitget":      {"maker": 0.1,  "taker": 0.1},
    "kraken":      {"maker": 0.16, "taker": 0.26},
    "coinbase":    {"maker": 0.4,  "taker": 0.6},
    "huobi":       {"maker": 0.2,  "taker": 0.2},
    "poloniex":    {"maker": 0.2,  "taker": 0.2},
    "bitfinex":    {"maker": 0.1,  "taker": 0.2},
    "whitebit":    {"maker": 0.1,  "taker": 0.1},
    "exmo":        {"maker": 0.3,  "taker": 0.3},
    "bingx":       {"maker": 0.1,  "taker": 0.1},
}

EXCHANGE_CLASSES = {
    "binance": ccxt.binance,
    "bybit": ccxt.bybit,
    "okx": ccxt.okx,
    "kucoin": ccxt.kucoin,
    "gate": ccxt.gate,
    "mexc": ccxt.mexc,
    "bitget": ccxt.bitget,
    "kraken": ccxt.kraken,
    "coinbase": ccxt.coinbase,
    "huobi": ccxt.huobi,
    "poloniex": ccxt.poloniex,
    "bitfinex": ccxt.bitfinex,
    "whitebit": ccxt.whitebit,
    "exmo": ccxt.exmo,
    "bingx": ccxt.bingx,
}

EXCHANGES = {name: cls() for name, cls in EXCHANGE_CLASSES.items()}

SYMBOLS = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "DOGE/USDT",
    "ADA/USDT", "BNB/USDT", "DOT/USDT", "TRX/USDT", "LTC/USDT",
    "AVAX/USDT", "LINK/USDT", "ATOM/USDT", "ETC/USDT", "UNI/USDT",
    "MATIC/USDT", "APT/USDT", "ARB/USDT", "OP/USDT", "SUI/USDT",
    "NEAR/USDT", "FIL/USDT", "AAVE/USDT", "EOS/USDT", "XTZ/USDT",
    "RUNE/USDT", "FTM/USDT", "KAVA/USDT", "GALA/USDT", "PEPE/USDT",
    "SHIB/USDT", "CRV/USDT", "SNX/USDT", "1INCH/USDT", "ZIL/USDT",
    "ENJ/USDT", "CHZ/USDT", "DYDX/USDT", "IMX/USDT", "MASK/USDT",
    "SAND/USDT", "MANA/USDT", "FLOW/USDT", "HBAR/USDT", "QNT/USDT",
    "ICP/USDT", "STX/USDT", "WOO/USDT", "LDO/USDT", "INJ/USDT"
]


def fetch_all_prices():
    prices = {}

    for ex_name, ex in EXCHANGES.items():
        for symbol in SYMBOLS:
            try:
                ticker = ex.fetch_ticker(symbol)
                last = ticker.get("last")
                if last:
                    prices.setdefault(symbol, {})[ex_name] = last
            except Exception:
                continue

    return prices


def calc_fees(buy_ex, sell_ex, mode):
    maker_buy = FEES[buy_ex]["maker"]
    taker_buy = FEES[buy_ex]["taker"]
    maker_sell = FEES[sell_ex]["maker"]
    taker_sell = FEES[sell_ex]["taker"]

    if mode == "taker":
        return taker_buy + taker_sell

    if mode == "maker_taker":
        return maker_buy + taker_sell

    if mode == "both":
        return min(
            taker_buy + taker_sell,
            maker_buy + taker_sell
        )

    return taker_buy + taker_sell


def find_arbitrage(prices, fee_mode="taker"):
    opps = []

    for symbol, ex_prices in prices.items():
        if len(ex_prices) < 2:
            continue

        items = list(ex_prices.items())

        for buy_ex, buy_price in items:
            for sell_ex, sell_price in items:
                if buy_ex == sell_ex:
                    continue

                spread = (sell_price - buy_price) / buy_price * 100

                fees = calc_fees(buy_ex, sell_ex, fee_mode)
                net = spread - fees

                if net > -5:
                    opps.append({
                        "pair": symbol,
                        "buy_exchange": buy_ex,
                        "buy_price": buy_price,
                        "sell_exchange": sell_ex,
                        "sell_price": sell_price,
                        "raw_spread": spread,
                        "fees": fees,
                        "net_spread": net,
                    })

    return opps

