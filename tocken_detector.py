import asyncio
import aiohttp
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load env vars from config file
load_dotenv(dotenv_path="config.env")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

BASE_URL = "https://api.helius.xyz/v0/addresses"
SCAN_INTERVAL = 3

MONITOR_ADDRESSES = {
    "Token Program":       "TokenkegQfeZyiNwAJbNbGKPFXCWvBvf9Ss623VQ5DA",
    "Raydium AMM":         "RVKd61ztZW9DQjhwvZ3ZzBivGiCuQ4Cuj3kYVfCR7c5",
    "Orca Whirlpools":     "whirLbENtLpzWobY9haJ9YQ2uJCNJhznfxMTr7nEQTf",
    "Meteora":             "Z3kgbRyVXETPBxM1Yk9zHqv7qL7U3UhGp8yzfGctX1v",
    "Lifinity":            "LifnCkKq1UXnPxfmsYQ4egmMp8JZQm7NvCDybNqCYvG",
    "Phoenix Orderbook":   "4ckmDgGzLYLyL6tY1U25YzFaCrAbzRYcnm1Xf2g3Syst",
    "Saber":               "SaberESsHnJptWVA4z7hEFS4wCWv95fkt2yC7oDwP23",
}

seen_tokens = set()

def log(msg: str):
    print(f"[{datetime.now().isoformat()}] {msg}")

async def fetch_transactions(session, address_name, address, limit=100):
    log(f"🔎 Scanning address '{address_name}' ({address})...")
    url = f"{BASE_URL}/{address}/transactions?api-key={HELIUS_API_KEY}&limit={limit}"
    async with session.get(url) as resp:
        if resp.status != 200:
            raise Exception(f"Failed with status {resp.status}")
        data = await resp.json()
        log(f"✅ Retrieved {len(data)} transactions from {address_name}")
        return address_name, data

def detect_new_tokens(address_name, transactions):
    new_tokens = []
    now = datetime.now(timezone.utc)
    for tx in transactions:
        if "tokenTransfers" in tx:
            for transfer in tx["tokenTransfers"]:
                if transfer.get("type") == "mint":
                    mint = transfer.get("mint")
                    if mint and mint not in seen_tokens:
                        timestamp = datetime.fromtimestamp(tx["timestamp"], tz=timezone.utc)
                        age_minutes = (now - timestamp).total_seconds() / 60.0
                        new_tokens.append({
                            "mint_address": mint,
                            "timestamp": timestamp.isoformat(),
                            "age_minutes": round(age_minutes, 2),
                            "source": address_name
                        })
                        seen_tokens.add(mint)
    return new_tokens

async def scan_once(session):
    log("🚀 Starting new scan cycle...")
    tasks = [
        fetch_transactions(session, name, addr)
        for name, addr in MONITOR_ADDRESSES.items()
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for (name, result) in zip(MONITOR_ADDRESSES.keys(), results):
        if isinstance(result, Exception):
            log(f"❌ Error while scanning '{name}': {result}")
            continue

        address_name, transactions = result
        tokens = detect_new_tokens(address_name, transactions)
        if tokens:
            for token in tokens:
                log(f"🪙 New Token Detected from {token['source']}: {token['mint_address']} at {token['timestamp']} ({token['age_minutes']} min ago)")
        else:
            log(f"ℹ️ No new tokens detected for {address_name}.")

    log("🕒 Scan cycle complete.\n")

async def continuous_scan():
    log("📡 SolScanner initialized and running.")
    async with aiohttp.ClientSession() as session:
        while True:
            await scan_once(session)
            await asyncio.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(continuous_scan())
    except KeyboardInterrupt:
        log("👋 Graceful shutdown.")
