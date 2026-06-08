from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from database.db import execute


ROOT_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = ROOT_DIR / "exports"


class ExportService:
    def __init__(self) -> None:
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    def _filename(self, suffix: str) -> Path:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return EXPORT_DIR / f"job_results_{stamp}.{suffix}"

    def export_csv(self, df: pd.DataFrame) -> Path:
        path = self._filename("csv")
        df.to_csv(path, index=False)
        self._log_export("CSV", path, len(df))
        return path

    def export_excel(self, df: pd.DataFrame) -> Path:
        path = self._filename("xlsx")
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Jobs")
            worksheet = writer.sheets["Jobs"]
            for column_cells in worksheet.columns:
                max_length = max(len(str(cell.value or "")) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(max_length + 3, 45)
        self._log_export("Excel", path, len(df))
        return path

    def export_pdf(self, df: pd.DataFrame) -> Path:
        path = self._filename("pdf")
        display_df = df.copy()
        for column in display_df.columns:
            display_df[column] = display_df[column].astype(str).str.slice(0, 42)

        data = [list(display_df.columns)] + display_df.fillna("").values.tolist()
        pdf = SimpleDocTemplate(str(path), pagesize=landscape(letter), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        table = Table(data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f7fb")]),
                ]
            )
        )
        pdf.build([table])
        self._log_export("PDF", path, len(df))
        return path

    def _log_export(self, export_type: str, path: Path, row_count: int) -> None:
        execute(
            "INSERT INTO exports (export_type, file_path, row_count) VALUES (?, ?, ?)",
            (export_type, str(path), row_count),
        )
