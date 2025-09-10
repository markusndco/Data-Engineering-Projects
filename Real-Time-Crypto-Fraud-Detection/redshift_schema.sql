-- Redshift Time-Series Schema for Crypto Transactions
CREATE SCHEMA IF NOT EXISTS crypto;

-- Raw staging (COPY from S3)
CREATE TABLE IF NOT EXISTS crypto.stg_transactions_json (
  raw_json VARCHAR(MAX)
);

-- Canonical table (partitioned by dt via sortkey, not true partition in RS)
CREATE TABLE IF NOT EXISTS crypto.fact_transactions (
  event_id       VARCHAR(64)   ENCODE zstd,
  event_ts       TIMESTAMP     ENCODE az64,
  exchange       VARCHAR(32)   ENCODE zstd,
  symbol         VARCHAR(16)   ENCODE bytedict,
  side           VARCHAR(8)    ENCODE bytedict,
  price_usd      DOUBLE PRECISION ENCODE az64,
  qty            DOUBLE PRECISION ENCODE az64,
  notional_usd   DOUBLE PRECISION ENCODE az64,
  taker          BOOLEAN       ENCODE zstd,
  maker_fee_bps  DOUBLE PRECISION ENCODE az64,
  country        VARCHAR(8)    ENCODE bytedict,
  wallet_from    VARCHAR(64)   ENCODE zstd,
  wallet_to      VARCHAR(64)   ENCODE zstd,
  status         VARCHAR(16)   ENCODE bytedict,
  chain          VARCHAR(16)   ENCODE bytedict,
  block_height   BIGINT        ENCODE az64,
  tx_latency_ms  INTEGER       ENCODE az64,
  ip_hash        VARCHAR(128)  ENCODE zstd,
  dt             DATE          ENCODE zstd,
  hour           SMALLINT      ENCODE zstd
)
DISTSTYLE KEY
DISTKEY(event_id)
SORTKEY(dt, symbol, event_ts);

-- Dimension: symbols
CREATE TABLE IF NOT EXISTS crypto.dim_symbol (
  symbol         VARCHAR(16) PRIMARY KEY,
  base_asset     VARCHAR(16),
  quote_asset    VARCHAR(16),
  tick_size      DOUBLE PRECISION
);

-- Aggregates for low-latency inference windows
CREATE MATERIALIZED VIEW IF NOT EXISTS crypto.mv_symbol_5m AS
SELECT
  symbol,
  date_trunc('minute', event_ts) AS minute,
  COUNT(*) AS events,
  SUM(notional_usd) AS notional_usd,
  AVG(price_usd) AS avg_price_usd
FROM crypto.fact_transactions
WHERE event_ts >= dateadd(day, -7, getdate())
GROUP BY 1,2
WITH NO DATA;

-- Feature View for fraud scoring
CREATE VIEW IF NOT EXISTS crypto.vw_fraud_features AS
SELECT
  t.event_id,
  t.symbol,
  t.price_usd,
  t.qty,
  t.notional_usd,
  (CASE WHEN t.tx_latency_ms > 2000 THEN 1 ELSE 0 END) AS high_latency_flag,
  (CASE WHEN t.maker_fee_bps > 10 THEN 1 ELSE 0 END) AS high_fee_flag,
  (CASE WHEN t.country IN ('RU','KP','IR') THEN 1 ELSE 0 END) AS high_risk_geo_flag,
  t.dt,
  t.event_ts
FROM crypto.fact_transactions t;
