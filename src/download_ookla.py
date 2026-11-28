"""Downloading Cameroon's Ookla speed-test tiles, quarter by quarter.

Reads Ookla's global Parquet files remotely with DuckDB and keeps only
tiles inside the zoom-8 squares covering Cameroon. Files already
downloaded are skipped, so reruns only fetch new quarters.

Usage:
    python src/download_ookla.py          # all quarters
    python src/download_ookla.py --test   # one file only (fixed, 2024 Q1)
"""
import argparse
import csv
import json
import time
from datetime import date
from pathlib import Path

import urllib.request
import urllib.error

import duckdb
import yaml

ROOT = Path(__file__).resolve().parent.parent
with open(ROOT / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

OUT_DIR = ROOT / config["paths"]["raw"] / "ookla"
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOG = ROOT / "reports" / "download_log.csv"
LOG.parent.mkdir(exist_ok=True)

ZOOM = config["ookla"]["filter_zoom"]
with open(ROOT / config["paths"]["interim"] / f"cameroon_quadkeys_z{ZOOM}.json",
          encoding="utf-8") as f:
    QUADKEYS = json.load(f)

BASE = config["ookla"]["base_url"]
COLUMNS = ", ".join(config["ookla"]["columns"])
PREFIXES = ", ".join(f"'{q}'" for q in QUADKEYS)


def url_for(net_type, year, quarter):
    month = (quarter - 1) * 3 + 1
    return (f"{BASE}/type={net_type}/year={year}/quarter={quarter}/"
            f"{year}-{month:02d}-01_performance_{net_type}_tiles.parquet")


def quarters_from(start_year, start_quarter):
    """Yield (year, quarter) from the start up to the current quarter."""
    today = date.today()
    current = (today.year, (today.month - 1) // 3 + 1)
    y, q = start_year, start_quarter
    while (y, q) <= current:
        yield y, q
        q += 1
        if q == 5:
            y, q = y + 1, 1


def is_not_found(error):
    msg = str(error)
    return "404" in msg or "Not Found" in msg or "NoSuchKey" in msg


GLOBAL_DIR = ROOT / config["paths"]["raw"] / "global"
GLOBAL_DIR.mkdir(parents=True, exist_ok=True)


def fetch_global(url, dest):
    """Download a global Ookla file to disk. Returns False if not published."""
    part = dest.with_suffix(".part")
    try:
        with urllib.request.urlopen(url, timeout=60) as resp, open(part, "wb") as f:
            total = int(resp.headers.get("Content-Length", 0))
            done = 0
            while chunk := resp.read(1024 * 1024):   # 1 MB at a time
                f.write(chunk)
                done += len(chunk)
                if total:
                    print(f"\r  downloading {done/1e6:,.0f} / {total/1e6:,.0f} MB",
                          end="", flush=True)
        print()
    except urllib.error.HTTPError as e:
        if part.exists():
            part.unlink()
        if e.code in (403, 404):
            return False
        raise
    except Exception:
        if part.exists():
            part.unlink()
        raise
    part.rename(dest)
    return True


def download_one(con, net_type, year, quarter):
    out = OUT_DIR / f"{net_type}_{year}_q{quarter}.parquet"
    if out.exists():
        print(f"  skip   {out.name} (already downloaded)")
        return "skipped"

    start = time.time()
    global_file = GLOBAL_DIR / f"{net_type}_{year}_q{quarter}_global.parquet"

    if not global_file.exists():
        if not fetch_global(url_for(net_type, year, quarter), global_file):
            return "not_published"

    tmp = out.with_suffix(".tmp")
    con.execute(f"""
        COPY (
            SELECT {COLUMNS},
                   '{net_type}' AS net_type,
                   {year} AS year,
                   {quarter} AS quarter
            FROM read_parquet('{global_file.as_posix()}')
            WHERE substr(quadkey, 1, {ZOOM}) IN ({PREFIXES})
        ) TO '{tmp.as_posix()}' (FORMAT PARQUET)
    """)
    tmp.rename(out)
    global_file.unlink()          # free the disk space

    rows, tests = con.execute(
        f"SELECT count(*), sum(tests) FROM read_parquet('{out.as_posix()}')"
    ).fetchone()
    seconds = round(time.time() - start)

    new_log = not LOG.exists()
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_log:
            w.writerow(["net_type", "year", "quarter", "rows", "tests",
                        "seconds", "downloaded_on"])
        w.writerow([net_type, year, quarter, rows, tests, seconds,
                    date.today().isoformat()])

    print(f"  saved  {out.name}: {rows:,} tiles, {tests:,} tests, {seconds}s")
    return "saved"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true",
                        help="download only fixed 2024 Q1")
    args = parser.parse_args()

    con = duckdb.connect()
    

    study = config["study"]
    types = ["fixed"] if args.test else study["net_types"]

    for net_type in types:
        print(f"\n=== {net_type} ===")
        for year, quarter in quarters_from(study["start_year"], study["start_quarter"]):
            status = download_one(con, net_type, year, quarter)
            if status == "not_published":
                print(f"  stop   {year} Q{quarter} not published yet")
                break
            if args.test:
                return


if __name__ == "__main__":
    main()