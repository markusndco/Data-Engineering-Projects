"""
Lambda — Real-Time Fraud Detection Alerting
-------------------------------------------
Triggered by Kinesis (via Event Source Mapping) to inspect records and publish
alerts to SNS if thresholds are breached. Designed for constant-time execution
and graceful degradation under burst traffic.

Security:
- Principle of Least Privilege IAM for SNS publish and CloudWatch PutMetricData
- KMS-encrypted environment variables for secrets

Author: Kiran Ranganalli
Last Updated: Aug 2025
"""
import os
import json
import logging
from decimal import Decimal

import boto3

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:us-west-2:123456789012:FraudAlerts")

logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
log = logging.getLogger("fraud_lambda")

sns = boto3.client("sns")
cloudwatch = boto3.client("cloudwatch")

THRESHOLDS = {
    "HIGH_VALUE_AMOUNT": float(os.getenv("HIGH_VALUE_AMOUNT", "1000")),
    "FAILED_PAYMENT_RATIO": float(os.getenv("FAILED_PAYMENT_RATIO", "0.15")),
    "GEO_MISMATCH_WEIGHT": float(os.getenv("GEO_MISMATCH_WEIGHT", "0.2")),
    "FRAUD_SCORE_ALERT": float(os.getenv("FRAUD_SCORE_ALERT", "0.6"))
}

def publish_metric(name: str, value: float):
    try:
        cloudwatch.put_metric_data(
            Namespace="Ecommerce/Realtime",
            MetricData=[
                {
                    "MetricName": name,
                    "Value": value,
                    "Unit": "Count"
                }
            ]
        )
    except Exception as e:
        log.warning(f"Metric publish failed: {e}")

def notify(subject: str, message: str):
    log.warning(f"ALERT: {subject} | {message}")
    try:
        sns.publish(TopicArn=SNS_TOPIC_ARN, Subject=subject, Message=message)
    except Exception as e:
        log.error(f"SNS publish failed: {e}")

def parse_record(rec) -> dict:
    # Kinesis event
    payload = rec.get("kinesis", {}).get("data")
    if not payload:
        return {}
    import base64
    decoded = base64.b64decode(payload).decode("utf-8")
    try:
        obj = json.loads(decoded)
    except json.JSONDecodeError:
        return {}
    return obj

def lambda_handler(event, context):
    failed_payments = 0
    total_payments = 0
    high_value_count = 0
    alerts = 0

    for rec in event.get("Records", []):
        obj = parse_record(rec)
        if not obj:
            continue

        event_type = obj.get("event_type")
        amount = float(obj.get("amount", 0.0))
        success = bool(obj.get("success", True))
        currency = obj.get("currency", "USD")
        region = obj.get("region", "NA")

        # Update counters
        if event_type in ("payment_attempt", "purchase"):
            total_payments += 1
            if not success:
                failed_payments += 1
        if amount >= THRESHOLDS["HIGH_VALUE_AMOUNT"]:
            high_value_count += 1

        # Simple fraud scoring logic (matches Spark job semantics)
        is_high_value = amount > 500
        is_geo_mismatch = (region in ("EU","APAC")) and (currency == "USD")
        fraud_score = (0.4 if is_high_value else 0.0) + (0.5 if (event_type == "payment_attempt" and not success) else 0.0) + (0.2 if is_geo_mismatch else 0.0)

        if fraud_score >= THRESHOLDS["FRAUD_SCORE_ALERT"]:
            alerts += 1
            notify(
                subject="[Fraud] Suspicious transaction pattern detected",
                message=json.dumps({"event": obj, "fraud_score": fraud_score})
            )

    # Ratios + operational metrics
    failure_ratio = (failed_payments / total_payments) if total_payments else 0.0
    publish_metric("FailedPaymentRatio", failure_ratio)
    publish_metric("HighValueCount", high_value_count)
    publish_metric("AlertsSent", alerts)

    # Alert on elevated failure ratio at the batch level
    if failure_ratio >= THRESHOLDS["FAILED_PAYMENT_RATIO"]:
        notify(
            subject="[Fraud] Elevated failure ratio",
            message=f"Failed/Total payments {failed_payments}/{total_payments} = {failure_ratio:.2f}"
        )

    return {"statusCode": 200, "body": json.dumps({"alerts": alerts, "failure_ratio": failure_ratio})}
