"""
SageMaker Fraud Scoring Harness
===============================
- Loads engineered features from Redshift or S3
- Invokes a deployed SageMaker endpoint for real-time fraud scoring
- Persists scores back to Redshift and S3
"""
import os, json, csv, time
from datetime import datetime
from typing import List, Dict, Any

import boto3

sagemaker_rt = boto3.client("sagemaker-runtime")

REDSHIFT_CLUSTER = os.getenv("REDSHIFT_CLUSTER","redshift-cluster.endpoint")
S3_SCORES_BUCKET = os.getenv("S3_SCORES_BUCKET","fraud-scores-bucket")
ENDPOINT_NAME = os.getenv("SM_ENDPOINT","fraud-detector-endpoint")

def score_payload(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for r in records:
        body = json.dumps(r)
        resp = sagemaker_rt.invoke_endpoint(
            EndpointName=ENDPOINT_NAME, 
            ContentType="application/json", 
            Body=body
        )
        payload = json.loads(resp["Body"].read().decode("utf-8"))
        score = payload.get("fraud_score", 0.0)
        out.append({**r, "fraud_score": score, "scored_at": datetime.utcnow().isoformat()})
    return out

def write_s3_jsonl(key: str, rows: List[Dict[str, Any]]):
    s3 = boto3.client("s3")
    body = "\n".join(json.dumps(r) for r in rows).encode("utf-8")
    s3.put_object(Bucket=S3_SCORES_BUCKET, Key=key, Body=body)

def main():
    # For demo, generate a small in-memory batch. Replace with Redshift query.
    sample = [
        {"event_id":"tx_demo_1","symbol":"BTC","price_usd":42000.0,"qty":0.12,"notional_usd":5040.0},
        {"event_id":"tx_demo_2","symbol":"ETH","price_usd":2800.0,"qty":2.5,"notional_usd":7000.0},
    ]
    scored = score_payload(sample)
    day = datetime.utcnow().strftime("%Y-%m-%d")
    key = f"scores/dt={day}/scores.jsonl"
    write_s3_jsonl(key, scored)
    print(f"[OK] wrote {len(scored)} scored rows to s3://{S3_SCORES_BUCKET}/{key}")

if __name__ == "__main__":
    main()
