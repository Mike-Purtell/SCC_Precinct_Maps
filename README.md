# Santa Clara County ROV Precinct Maps (2026-11-02)

Scripts and tracking data for downloading the precinct map PDFs published by the Santa Clara County Registrar of Voters (ROV).

## Contents

| File / Folder | Description |
|---|---|
| `ROV_Precinct_Map_URLs_2026_11_02.xlsx` | One row per precinct: `PRECINCT` (4 digits), `URL` of the map PDF, and `Downloaded` (`OK` or `MISSING`). |
| `Download_PDFs.py` | Downloads the PDF for each row's `URL` into `PDFs/`. |
| `update_download_result_2206_11_02.py` | Sets the `Downloaded` column to `OK` or `MISSING` based on what is in `PDFs/`. |
| `Download_Precinct_Maps_Notes_2026_11_02.txt` | Working notes. |
| `PDFs/` | Downloaded precinct maps (e.g. `pct_2001.pdf`). |

## Usage

Requires Python 3 and:

```
python -m pip install polars fastexcel openpyxl requests
```

1. **Download the maps**: `python Download_PDFs.py`
   - Set `LIMIT` near the top of the script to a small number (e.g. `10`) to test, or `None` to download all rows.
   - Whitespace in file names is replaced with underscores. Existing files are skipped, and responses that aren't PDFs are reported as failures.
2. **Update the spreadsheet**: `python update_download_result_2206_11_02.py`
   - A precinct is `OK` if a file in `PDFs/` has that precinct number as the 4 digits just before `.pdf`; otherwise it is `MISSING`.
   - Close the Excel file first, since the script saves over it.

## Notes

- Some URLs return 404 because the map is not on the server (for example precinct 2006), which is why some precincts are `MISSING`.
