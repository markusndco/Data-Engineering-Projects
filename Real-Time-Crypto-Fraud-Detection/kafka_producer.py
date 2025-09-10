"""
Kafka Producer — Synthetic Crypto Transactions
=============================================
Generates high-throughput crypto transaction events and publishes to Kafka.
Designed for load testing and pipeline demos for fraud detection / trading sims.

Usage:
  python kafka_producer.py --brokers localhost:9092 --topic crypto.transactions --eps 500

Notes:
- Idempotent producer enabled
- Batches and compression set for high throughput
- Schema evolution hooks included
"""

import argparse
import json
import os
import random
import string
import time
from datetime import datetime, timezone
from typing import Dict, Any

try:
    from confluent_kafka import Producer
except ImportError:
    Producer = None  # fallback for environments without confluent_kafka

CURRENCIES = ["BTC","ETH","USDT","SOL","BNB","XRP","ADA","DOGE","DOT","LTC"]
EXCHANGES = ["binance","coinbase","kraken","bitfinex","bybit","okx","upbit"]
COUNTRIES = ["US","GB","DE","SG","IN","JP","BR","CA","AU","AE"]
SIDE = ["buy","sell"]
STATUS = ["filled","partial","rejected","canceled","pending"]

def rand_wallet() -> str:
    return "0x" + "".join(random.choices("0123456789abcdef", k=40))

def rand_txn_id() -> str:
    return "tx_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=24))

def rand_amount(symbol:str) -> float:
    base = random.uniform(0.0001, 25.0)
    if symbol == "USDT": base *= 2000
    return round(base, 8)

def sample_transaction() -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    symbol = random.choice(CURRENCIES)
    price_usd = round(random.uniform(0.1, 65000.0), 2)
    qty = rand_amount(symbol)
    notional = round(price_usd * qty, 2)
    return {
        "event_id": rand_txn_id(),
        "ts": ts,
        "exchange": random.choice(EXCHANGES),
        "symbol": symbol,
        "side": random.choice(SIDE),
        "price_usd": price_usd,
        "qty": qty,
        "notional_usd": notional,
        "taker": random.choice([True, False]),
        "maker_fee_bps": round(random.uniform(0.5, 15.0), 2),
        "country": random.choice(COUNTRIES),
        "wallet_from": rand_wallet(),
        "wallet_to": rand_wallet(),
        "status": random.choices(STATUS, weights=[70,10,5,5,10])[0],
        "chain": random.choice(["eth","sol","bsc","tron","polygon","btc"]),
        "block_height": random.randint(1_000_000, 20_000_000),
        "tx_latency_ms": random.randint(5, 3000),
        "ip_hash": "".join(random.choices("abcdef0123456789", k=64)),
        "schema_ver": "v1"
    }

def make_producer(brokers: str) -> Any:
    if Producer is None:
        print("[WARN] confluent_kafka not available. Running in print mode.")
        return None
    conf = {
        "bootstrap.servers": brokers,
        "enable.idempotence": True,
        "acks": "all",
        "compression.type": "lz4",
        "linger.ms": 50,
        "batch.num.messages": 10000,
        "message.timeout.ms": 30000,
        "socket.keepalive.enable": True,
    }
    return Producer(conf)

def delivery(err, msg):
    if err:
        print(f"[DELIVERY_ERROR] {err}")
    else:
        pass  # could collect metrics

def run(args):
    p = make_producer(args.brokers)
    eps = max(1, args.eps)
    topic = args.topic
    print(f"[BOOT] producing to {topic} at ~{eps} events/sec; ctrl+c to stop")
    try:
        while True:
            start = time.time()
            for _ in range(eps):
                evt = sample_transaction()
                payload = json.dumps(evt)
                if p:
                    p.produce(topic, payload.encode("utf-8"), callback=delivery)
                else:
                    print(payload)
            if p:
                p.flush(0)
            elapsed = time.time() - start
            sleep_for = max(0.0, 1.0 - elapsed)
            time.sleep(sleep_for)
    except KeyboardInterrupt:
        print("\n[STOP] keyboard interrupt")
    finally:
        if p:
            p.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--brokers", default="localhost:9092")
    parser.add_argument("--topic", default="crypto.transactions")
    parser.add_argument("--eps", type=int, default=200)
    run(parser.parse_args())
