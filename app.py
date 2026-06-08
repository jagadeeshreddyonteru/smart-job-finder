from __future__ import annotations

import streamlit as st

from pages.analytics_page import render_analytics_page
from pages.dashboard import render_dashboard
from pages.exports import render_exports_page
from pages.search import render_search_page

st.set_page_config(page_title="AI Job Finder", layout="wide")


def main() -> None:
    st.sidebar.title("AI Job Finder")
    page = st.sidebar.radio("Navigation", ["Dashboard", "Search Jobs", "Analytics", "Exports"], label_visibility="collapsed")
    st.sidebar.caption("Uses public career links and approved data sources only.")

    if page == "Dashboard":
        render_dashboard()
    elif page == "Search Jobs":
        render_search_page()
    elif page == "Analytics":
        render_analytics_page()
    else:
        render_exports_page()


if __name__ == "__main__":
    main()
