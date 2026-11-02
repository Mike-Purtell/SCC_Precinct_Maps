import re
from pathlib import Path

import openpyxl

HERE = Path(__file__).parent
EXCEL = HERE / "ROV_Precinct_Map_URLs_2026_11_02.xlsx"
PDF_DIR = HERE / "PDFs"


def main():
    # Precinct number is the 4 digits immediately before .pdf
    found = set()
    for pdf in PDF_DIR.glob("*.pdf"):
        m = re.search(r"(\d{4})$", pdf.stem)
        if m:
            found.add(m.group(1))

    wb = openpyxl.load_workbook(EXCEL)
    ws = wb.active
    headers = {c.value: c.column for c in ws[1]}
    pct_col = headers["PRECINCT"]
    dl_col = headers["Downloaded"]

    ok = missing = 0
    for row in range(2, ws.max_row + 1):
        pct = ws.cell(row, pct_col).value
        if pct is None:
            continue
        status = "OK" if str(pct).strip() in found else "MISSING"
        ws.cell(row, dl_col).value = status
        if status == "OK":
            ok += 1
        else:
            missing += 1

    wb.save(EXCEL)
    print(f"Updated {EXCEL.name}: {ok} OK, {missing} MISSING")


if __name__ == "__main__":
    main()
