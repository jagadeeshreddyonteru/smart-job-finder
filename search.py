from __future__ import annotations

import pandas as pd
import streamlit as st

from services.company_service import CompanyService
from services.export_service import ExportService
from services.job_service import ROLE_KEYWORDS, JobService
from services.matching_service import MatchingService


def render_search_page() -> None:
    st.title("Search Jobs")

    company_service = CompanyService()
    locations = [""] + company_service.list_locations()

    col1, col2, col3 = st.columns([1, 1, 0.6])
    with col1:
        location_choice = st.selectbox("Location", locations, format_func=lambda item: item or "Any Location")
        custom_location = st.text_input("Custom Location", placeholder="Hyderabad, Bangalore, Chennai")
    with col2:
        keyword = st.selectbox("Role Filter", ROLE_KEYWORDS)
        custom_keyword = st.text_input("Custom Skill / Role", placeholder="Automation Tester, Power BI, Java")
    with col3:
        max_results = st.number_input("Max Results", min_value=10, max_value=500, value=100, step=10)

    resume_text = st.text_area("Optional Resume Skills", placeholder="Paste skills or resume summary to calculate match scores.")

    final_location = custom_location.strip() or location_choice
    final_keyword = custom_keyword.strip() or keyword

    if st.button("Search", type="primary", use_container_width=True):
        df = JobService().search_jobs(final_keyword, final_location, int(max_results))
        df = MatchingService().add_match_scores(df, resume_text)
        st.session_state["search_results"] = df
        st.success(f"{len(df)} jobs found")

    df = st.session_state.get("search_results", pd.DataFrame())
    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Apply Link": st.column_config.LinkColumn("Apply Link"),
                "Careers Page": st.column_config.LinkColumn("Careers Page"),
            },
        )

        export_col1, export_col2, export_col3 = st.columns(3)
        exporter = ExportService()
        with export_col1:
            if st.button("Export CSV", use_container_width=True):
                path = exporter.export_csv(df)
                st.success(f"Saved {path}")
        with export_col2:
            if st.button("Export Excel", use_container_width=True):
                path = exporter.export_excel(df)
                st.success(f"Saved {path}")
        with export_col3:
            if st.button("Export PDF", use_container_width=True):
                path = exporter.export_pdf(df)
                st.success(f"Saved {path}")
    else:
        st.info("Enter a location and role, then run a search.")
