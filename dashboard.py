from __future__ import annotations

import streamlit as st

from services.analytics import AnalyticsService
from services.company_service import CompanyService
from services.job_service import JobService


def render_dashboard() -> None:
    CompanyService().seed_companies()
    JobService().seed_jobs()
    analytics = AnalyticsService()
    metrics = analytics.summary_metrics()

    st.title("AI-Powered Location-Based Job Finder")
    st.caption("Find companies, current openings, public careers pages, and export-ready job reports.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Companies", metrics["companies"])
    col2.metric("Jobs", metrics["jobs"])
    col3.metric("Searches", metrics["searches"])
    col4.metric("Exports", metrics["exports"])

    left, right = st.columns(2)
    with left:
        location_df = analytics.jobs_by_location()
        if not location_df.empty:
            st.plotly_chart(analytics.location_chart(location_df), use_container_width=True)
    with right:
        role_df = analytics.jobs_by_role()
        if not role_df.empty:
            st.plotly_chart(analytics.role_chart(role_df), use_container_width=True)

    st.subheader("What This Version Collects")
    st.write(
        "Company names, public websites, official careers pages, job roles, experience, locations, "
        "apply links, and public hiring inboxes when the company publishes one."
    )
