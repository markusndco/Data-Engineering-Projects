"""
HDFS Ingestion Pipeline (Simplified)
- Validates raw CSV logs
- Creates dt/hr partition folder structure
- Writes partitioned CSV (stand-in for HDFS put)
"""
import os
import csv
from pathlib import Path
from datetime import datetime

LANDING_FILE = Path("sample_logs.csv")
OUT_ROOT = Path("out_raw")

def ensure(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def partition_path(ts: str) -> Path:
    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    hr = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%H")
    return OUT_ROOT / f"dt={dt}" / f"hr={hr}"

def ingest():
    ensure(OUT_ROOT)
    with open(LANDING_FILE) as f:
        reader = csv.DictReader(f)
        buffers = {}
        for row in reader:
            p = partition_path(row["event_time"])
            ensure(p)
            buffers.setdefault(p, []).append(row)

        for p, rows in buffers.items():
            out_file = p / "part-00001.csv"
            write_header = not out_file.exists()
            with open(out_file, "a", newline="") as wf:
                w = csv.DictWriter(wf, fieldnames=list(rows[0].keys()))
                if write_header: w.writeheader()
                w.writerows(rows)
            print(f"[OK] wrote {len(rows)} rows -> {out_file}")

if __name__ == "__main__":
    if not LANDING_FILE.exists():
        raise SystemExit("sample_logs.csv not found. Generate it first.")
    ingest()
