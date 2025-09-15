# FUNCIONES

import psycopg2
from datetime import datetime
import requests
import re
from variables import config

# -------------------------
# Guardar en DB
# -------------------------
def bbdd(pregunta, respuesta):
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    query = """
        INSERT INTO preguntas_respuestas (preguntas, respuestas, fechas)
        VALUES (%s, %s, %s)
        RETURNING id, preguntas, respuestas, fechas;
    """
    cursor.execute(query, (pregunta, respuesta, datetime.now()))
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return row

# -------------------------
# Detectar cripto en la pregunta (ids CoinGecko)
# -------------------------
_COINGECKO_IDS = {
    # Bitcoin
    "bitcoin": "bitcoin", "btc": "bitcoin", "bitcon": "bitcoin", "bitcón": "bitcoin",
    "bitoin": "bitcoin", "bitc": "bitcoin", "satoshi": "bitcoin",

    # Ethereum
    "ethereum": "ethereum", "eth": "ethereum", "ether": "ethereum",
    "etereum": "ethereum", "eterium": "ethereum", "etrum": "ethereum",

    # Cardano
    "cardano": "cardano", "ada": "cardano",
    "cardanoo": "cardano", "cardona": "cardano",

    # Solana
    "solana": "solana", "sol": "solana",
    "solnaa": "solana", "solnaa": "solana", "solan": "solana",

    # Ripple / XRP
    "ripple": "ripple", "xrp": "ripple",
    "riple": "ripple", "rippl": "ripple", "rippple": "ripple",

    # Dogecoin
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "dogcoin": "dogecoin", "dogge": "dogecoin", "dogi": "dogecoin",

    # Litecoin
    "litecoin": "litecoin", "ltc": "litecoin",
    "litecon": "litecoin", "litcoin": "litecoin", "litc": "litecoin",

    # Polkadot
    "polkadot": "polkadot", "dot": "polkadot",
    "polcadot": "polkadot", "polka": "polkadot", "polkdot": "polkadot",

    # Binance Coin
    "binance coin": "binancecoin", "bnb": "binancecoin",
    "binanse": "binancecoin", "binans": "binancecoin",

    # Tether
    "tether": "tether", "usdt": "tether",
    "tehter": "tether", "teter": "tether",

    # USD Coin
    "usd coin": "usd-coin", "usdc": "usd-coin",
    "us coin": "usd-coin", "usdcoin": "usd-coin",

    # Avalanche
    "avalanche": "avalanche-2", "avax": "avalanche-2",
    "avalanch": "avalanche-2", "avalancha": "avalanche-2",

    # Chainlink
    "chainlink": "chainlink", "link": "chainlink",
    "chanlink": "chainlink", "chainlin": "chainlink",

    # Polygon (Matic)
    "polygon": "matic-network", "matic": "matic-network",
    "poligon": "matic-network", "poligon": "matic-network",

    # Stellar
    "stellar": "stellar", "xlm": "stellar",
    "steler": "stellar", "estelar": "stellar",

    # Tron
    "tron": "tron", "trx": "tron",
    "tronn": "tron", "tronnn": "tron",

    # Shiba Inu
    "shiba inu": "shiba-inu", "shib": "shiba-inu",
    "shiva": "shiba-inu", "shibaa": "shiba-inu", "shibaaa": "shiba-inu",

    # Monero
    "monero": "monero", "xmr": "monero",
    "monerro": "monero", "monnero": "monero",

    # Cosmos
    "cosmos": "cosmos", "atom": "cosmos",
    "cosmus": "cosmos", "cosmoss": "cosmos",

    # Uniswap
    "uniswap": "uniswap", "uni": "uniswap",
    "uniswapp": "uniswap", "unyswap": "uniswap",
}


def detectar_cripto(pregunta: str):
    q = (pregunta or "").lower()
    # normalizar signos raros
    q = re.sub(r"[^\w\s\-]", " ", q)
    for key, cg_id in _COINGECKO_IDS.items():
        if re.search(rf"\b{re.escape(key)}\b", q):
            return cg_id
    return None

# -------------------------
# Datos de mercado (logo + cifras) desde CoinGecko
# -------------------------
def get_crypto_data(cg_id: str):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{cg_id}"
        resp = requests.get(
            url,
            timeout=15,
            headers={"accept": "application/json", "user-agent": "crypto-app/1.0"}
        )
        if resp.status_code == 200:
            data = resp.json() or {}
            md = data.get("market_data", {}) or {}
            image = data.get("image", {}) or {}
            return {
                "logo": image.get("large"),
                "precio_usd": (md.get("current_price") or {}).get("usd"),
                "marketcap_usd": (md.get("market_cap") or {}).get("usd"),
                "circulating_supply": md.get("circulating_supply"),
                "max_supply": md.get("max_supply"),
            }
        return {"error": f"HTTP {resp.status_code} en /coins/{cg_id}"}
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Histórico para gráfico (30 días, precio diario)
# -------------------------
def get_crypto_chart(cg_id: str, days: int = 30):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{cg_id}/market_chart"
        params = {"vs_currency": "usd", "days": str(days)}
        resp = requests.get(
            url,
            params=params,
            timeout=15,
            headers={"accept": "application/json", "user-agent": "crypto-app/1.0"}
        )
        if resp.status_code == 200:
            data = resp.json() or {}
            prices = data.get("prices") or []  # lista de [timestamp_ms, price]
            fechas = [p[0] for p in prices]
            precios = [p[1] for p in prices]
            return {"fechas": fechas, "precios": precios}
        return {"fechas": [], "precios": [], "error": f"HTTP {resp.status_code} market_chart"}
    except Exception as e:
        return {"fechas": [], "precios": [], "error": str(e)}

# -------------------------
# Limpiar respuesta LLM (opcional)
# -------------------------
import re as _re
def limpiar_respuesta(texto: str) -> str:
    if not texto:
        return ""
    # Evitar triples guiones que el modelo a veces pone
    texto = _re.sub(r"\n?---+\n?", "\n\n", texto)
    return texto.strip()
