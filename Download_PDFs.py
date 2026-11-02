'''
Download precinct map PDFs from the URLs listed in the Excel file.
No special web scraping is required; the URLs are directly listed in the Excel,
and were easy to create with an excel formula
'''

from pathlib import Path
from urllib.parse import urlparse, unquote

import polars as pl
import requests

LIMIT = None  # set to None to download all rows

HERE = Path(__file__).parent
EXCEL = HERE / "ROV_Precinct_Map_URLs_2026_11_02.xlsx"
OUT_DIR = HERE / "PDFs"


def main():
    OUT_DIR.mkdir(exist_ok=True)
    df = pl.read_excel(EXCEL)
    if LIMIT:
        df = df.head(LIMIT)

    ok = failed = 0
    with requests.Session() as session:
        for row in df.iter_rows(named=True):
            url = str(row["URL"]).strip()
            name = Path(unquote(urlparse(url).path)).name or f"{row['PRECINCT']}.pdf"
            name = "_".join(name.split())
            dest = OUT_DIR / name
            if dest.exists() and dest.stat().st_size > 0:
                print(f"SKIP (exists): {name}")
                ok += 1
                continue
            try:
                r = session.get(url, timeout=60)
                r.raise_for_status()
                if not r.content.startswith(b"%PDF"):
                    raise ValueError("response is not a PDF")
                dest.write_bytes(r.content)
                print(f"OK: {name} ({len(r.content):,} bytes)")
                ok += 1
            except Exception as e:
                print(f"FAIL: {url} -> {e}")
                failed += 1

    print(f"Done. {ok} succeeded, {failed} failed.")


if __name__ == "__main__":
    main()
