"""
Kinesis Ingestion Lambda
========================
- Consumes Kinesis records (crypto transactions)
- Validates & enriches
- Writes raw and curated objects to S3 (data lake), routes failures to DLQ (SNS/SQS)
- Emits CloudWatch metrics

Environment Variables:
  RAW_BUCKET, CURATED_BUCKET, DLQ_ARN
"""
import os, json, base64, gzip, boto3, hashlib, time, traceback
from datetime import datetime, timezone

s3 = boto3.client("s3")
sns = boto3.client("sns")
cloudwatch = boto3.client("cloudwatch")

RAW_BUCKET = os.getenv("RAW_BUCKET","kinesis-raw-bucket")
CURATED_BUCKET = os.getenv("CURATED_BUCKET","kinesis-curated-bucket")
DLQ_ARN = os.getenv("DLQ_ARN","")

def put_metric(name, value, unit="Count"):
    try:
        cloudwatch.put_metric_data(
            Namespace="StreamingCrypto",
            MetricData=[{
                "MetricName": name,
                "Timestamp": datetime.utcnow(),
                "Value": value,
                "Unit": unit
            }]
        )
    except Exception as e:
        print(f"[WARN] metric error: {e}")

def write_s3(bucket, key, body:bytes):
    s3.put_object(Bucket=bucket, Key=key, Body=body)

def publish_dlq(message: str, reason: str):
    if not DLQ_ARN: 
        print(f"[DLQ] {reason}: {message[:200]}")
        return
    sns.publish(TopicArn=DLQ_ARN, Message=json.dumps({"reason":reason,"payload":message}))

def validate(evt: dict) -> bool:
    required = ["event_id","ts","symbol","price_usd","qty","wallet_from","wallet_to"]
    for k in required:
        if k not in evt or evt[k] in (None,""):
            return False
    return True

def enrich(evt: dict) -> dict:
    evt["ingested_at"] = datetime.now(timezone.utc).isoformat()
    evt["partition_dt"] = evt["ts"][:10]  # YYYY-MM-DD
    evt["region"] = evt.get("country","US")
    evt["notional_bucket"] = "large" if evt.get("notional_usd",0) > 100000 else "small"
    evt["fingerprint"] = hashlib.sha256((evt["wallet_from"]+evt["wallet_to"]).encode()).hexdigest()
    return evt

def handler(event, context):
    ok, bad = 0, 0
    for rec in event.get("Records", []):
        try:
            data_b64 = rec["kinesis"]["data"]
            raw = base64.b64decode(data_b64)
            # Payloads may be gzipped upstream; try-decompress
            try:
                payload = gzip.decompress(raw).decode("utf-8")
            except Exception:
                payload = raw.decode("utf-8")
            evt = json.loads(payload)
            if not validate(evt):
                bad += 1
                publish_dlq(payload, "validation_failed")
                continue
            evt = enrich(evt)
            dt = evt["partition_dt"]
            # write raw
            raw_key = f"raw/dt={dt}/{evt['event_id']}.json"
            write_s3(RAW_BUCKET, raw_key, json.dumps(evt).encode("utf-8"))
            # write curated partitioned parquet via Firehose or here as JSONL (demo)
            curated_key = f"curated/dt={dt}/symbol={evt['symbol']}/{evt['event_id']}.json"
            write_s3(CURATED_BUCKET, curated_key, json.dumps(evt).encode("utf-8"))
            ok += 1
        except Exception as e:
            bad += 1
            traceback.print_exc()
            publish_dlq(str(rec)[:2000], "exception")
    put_metric("RecordsOK", ok)
    put_metric("RecordsBad", bad)
    return {"ok": ok, "bad": bad}
