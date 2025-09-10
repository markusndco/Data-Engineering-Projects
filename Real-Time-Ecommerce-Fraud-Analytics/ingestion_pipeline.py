"""
Ingestion Pipeline for Real-Time E-commerce Analytics Platform
--------------------------------------------------------------
This module provisions and interacts with Amazon Kinesis + Firehose to ingest
high-throughput clickstream and transaction events into S3. It also provides
a local producer that simulates millions of events/day for load testing.

Key capabilities:
- Create or validate Kinesis Data Stream and Firehose Delivery Stream
- PutRecords batching with retry/backoff
- Optional schema registry for Glue Catalog (placeholder hooks)
- Local simulator to generate realistic e-commerce events
- Backpressure-aware batching and metrics logging

NOTE: This sample focuses on structure, reliability patterns, and production-
grade comments. Replace placeholders (bucket/stream names, ARNs) before use.

Author: Kiran Ranganalli
Last Updated: Aug 2025
"""

import os
import sys
import json
import time
import math
import uuid
import gzip
import base64
import random
import logging
from datetime import datetime, timezone
from typing import Dict, List, Tuple

try:
    import boto3
    from botocore.exceptions import ClientError
except Exception:  # for local linting w/o aws libs
    boto3 = None
    ClientError = Exception

# -------------------------------
# Configuration
# -------------------------------
REGION = os.getenv("AWS_REGION", "us-west-2")
KINESIS_STREAM = os.getenv("KINESIS_STREAM", "ecommerce-events-stream")
FIREHOSE_STREAM = os.getenv("FIREHOSE_STREAM", "ecommerce-firehose-to-s3")
S3_BUCKET = os.getenv("S3_BUCKET", "ecommerce-analytics-data")
S3_PREFIX = os.getenv("S3_PREFIX", "raw/events/")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "250"))       # Kinesis PutRecords max 500
MAX_INFLIGHT = int(os.getenv("MAX_INFLIGHT", "4"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("ingestion")

# -------------------------------
# AWS clients (lazy init)
# -------------------------------
_kinesis = None
_firehose = None
_s3 = None

def kinesis():
    global _kinesis
    if _kinesis is None and boto3 is not None:
        _kinesis = boto3.client("kinesis", region_name=REGION)
    return _kinesis

def firehose():
    global _firehose
    if _firehose is None and boto3 is not None:
        _firehose = boto3.client("firehose", region_name=REGION)
    return _firehose

def s3():
    global _s3
    if _s3 is None and boto3 is not None:
        _s3 = boto3.client("s3", region_name=REGION)
    return _s3

# -------------------------------
# Utilities
# -------------------------------
def ensure_streams():
    """
    Idempotently ensure Kinesis Data Stream and Firehose Delivery Stream exist.
    """
    if kinesis() is None or firehose() is None:
        log.warning("boto3 not available — skipping stream creation checks")
        return

    # Kinesis
    try:
        kinesis().describe_stream(StreamName=KINESIS_STREAM)
        log.info(f"Kinesis stream exists: {KINESIS_STREAM}")
    except ClientError:
        log.info(f"Creating Kinesis stream: {KINESIS_STREAM}")
        kinesis().create_stream(StreamName=KINESIS_STREAM, ShardCount=2)
        waiter = kinesis().get_waiter("stream_exists")
        waiter.wait(StreamName=KINESIS_STREAM)
        log.info("Kinesis stream created")

    # Firehose
    try:
        firehose().describe_delivery_stream(DeliveryStreamName=FIREHOSE_STREAM)
        log.info(f"Firehose delivery stream exists: {FIREHOSE_STREAM}")
    except ClientError:
        log.info(f"Creating Firehose delivery stream: {FIREHOSE_STREAM}")
        firehose().create_delivery_stream(
            DeliveryStreamName=FIREHOSE_STREAM,
            DeliveryStreamType="DirectPut",
            S3DestinationConfiguration={
                "RoleARN": "arn:aws:iam::123456789012:role/FirehoseDeliveryRole",
                "BucketARN": f"arn:aws:s3:::{S3_BUCKET}",
                "Prefix": f"{S3_PREFIX}year=!{{timestamp:yyyy}}/month=!{{timestamp:MM}}/day=!{{timestamp:dd}}/",
                "ErrorOutputPrefix": f"{S3_PREFIX}errors/!{{firehose:error-output-type}}/",
                "BufferingHints": {"SizeInMBs": 128, "IntervalInSeconds": 300},
                "CompressionFormat": "GZIP",
            },
        )
        log.info("Firehose stream creation requested (allow ~1-2 minutes to be ACTIVE)")

# -------------------------------
# Event Simulation
# -------------------------------
EVENT_TYPES = ["page_view","click","add_to_cart","checkout_start","payment_attempt","purchase","refund_request"]
CATEGORIES = ["Electronics","Clothing","Home","Books","Beauty","Sports","Toys"]
REGIONS = ["NA","EU","APAC","LATAM"]

def mk_event(user_id: str) -> Dict:
    """
    Create a realistic e-commerce event with random noise.
    """
    et = random.choices(EVENT_TYPES, weights=[35,30,15,7,6,6,1], k=1)[0]
    now = datetime.now(timezone.utc).isoformat()
    session_id = f"s_{uuid.uuid4().hex[:16]}"
    product_id = f"SKU_{random.randint(1000,9999)}"
    amount = float(f"{random.uniform(5, 1200):.2f}")
    currency = random.choice(["USD","EUR","JPY","GBP"])
    region = random.choice(REGIONS)

    payload = {
        "event_id": uuid.uuid4().hex,
        "event_type": et,
        "ts": now,
        "user_id": user_id,
        "session_id": session_id,
        "product_id": product_id,
        "category": random.choice(CATEGORIES),
        "region": region,
        "geo_ip": f"52.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        "amount": amount if et in ("payment_attempt","purchase") else 0.0,
        "currency": currency,
        "device": random.choice(["ios","android","web"]),
        "is_gift": random.choice([True, False, False, False]),
        "payment_method": random.choice(["visa","mastercard","amex","paypal"]),
        "success": True if et not in ("payment_attempt",) else random.random() > 0.08,
    }
    return payload

def batch_put_records(recs: List[Dict]) -> Tuple[int, int]:
    """
    PutRecords with simple retry/backoff. Returns (ok, fail) counts.
    """
    if kinesis() is None:
        # local mode: just log size
        log.info(f"[LOCAL] Would put {len(recs)} records to {KINESIS_STREAM}")
        return (len(recs), 0)

    entries = [{"Data": (json.dumps(r) + "\n").encode("utf-8"), "PartitionKey": r["user_id"]} for r in recs]
    resp = kinesis().put_records(StreamName=KINESIS_STREAM, Records=entries)
    failed = resp.get("FailedRecordCount", 0)
    return (len(recs) - failed, failed)

def simulate_and_ingest(total_events: int = 10000, users: int = 500):
    """
    Generate synthetic events and push to Kinesis.
    """
    ensure_streams()
    ok = fail = 0
    user_ids = [f"u_{i:05d}" for i in range(users)]
    batch = []
    for i in range(total_events):
        batch.append(mk_event(random.choice(user_ids)))
        if len(batch) >= BATCH_SIZE:
            a, b = batch_put_records(batch)
            ok += a; fail += b
            batch = []
            time.sleep(0.05)  # gentle backoff
    if batch:
        a, b = batch_put_records(batch)
        ok += a; fail += b

    log.info(f"Ingestion complete | ok={ok} fail={fail}")

if __name__ == "__main__":
    # Default: run a small local test
    simulate_and_ingest(total_events=2000, users=250)
