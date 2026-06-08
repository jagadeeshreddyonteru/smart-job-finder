from __future__ import annotations

from pathlib import Path

import streamlit as st

from database.db import fetch_all, init_db


def render_exports_page() -> None:
    init_db()
    st.title("Exports")
    rows = fetch_all(
        """
        SELECT export_type AS Type, file_path AS File, row_count AS Rows, created_at AS Created
        FROM exports
        ORDER BY created_at DESC
        """
    )

    if not rows:
        st.info("No exported files yet. Export search results from the Search Jobs page.")
        return

    for row in rows:
        path = Path(row["File"])
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            col1.metric(row["Type"], f"{row['Rows']} rows")
            col2.write(str(path))
            col2.caption(row["Created"])
            if path.exists():
                col3.download_button(
                    "Download",
                    data=path.read_bytes(),
                    file_name=path.name,
                    use_container_width=True,
                )
            else:
                col3.warning("Missing")
