from __future__ import annotations

import streamlit as st

from services.analytics import AnalyticsService
from services.job_service import JobService


def render_analytics_page() -> None:
    JobService().seed_jobs()
    analytics = AnalyticsService()

    st.title("Analytics")

    location_df = analytics.jobs_by_location()
    role_df = analytics.jobs_by_role()
    recent_df = analytics.recent_searches()

    col1, col2 = st.columns(2)
    with col1:
        if not location_df.empty:
            st.plotly_chart(analytics.location_chart(location_df), use_container_width=True)
        else:
            st.info("No location data yet.")
    with col2:
        if not role_df.empty:
            st.plotly_chart(analytics.role_chart(role_df), use_container_width=True)
        else:
            st.info("No role data yet.")

    st.subheader("Recent Searches")
    if recent_df.empty:
        st.info("No searches recorded yet.")
    else:
        st.dataframe(recent_df, use_container_width=True, hide_index=True)
