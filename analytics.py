from __future__ import annotations

import pandas as pd
import plotly.express as px

from database.db import fetch_all, init_db


class AnalyticsService:
    def __init__(self) -> None:
        init_db()

    def summary_metrics(self) -> dict[str, int]:
        rows = fetch_all(
            """
            SELECT
                (SELECT COUNT(*) FROM companies) AS companies,
                (SELECT COUNT(*) FROM jobs) AS jobs,
                (SELECT COUNT(*) FROM searches) AS searches,
                (SELECT COUNT(*) FROM exports) AS exports
            """
        )
        return rows[0] if rows else {"companies": 0, "jobs": 0, "searches": 0, "exports": 0}

    def jobs_by_location(self) -> pd.DataFrame:
        return pd.DataFrame(
            fetch_all(
                """
                SELECT location AS Location, COUNT(*) AS Jobs
                FROM jobs
                GROUP BY location
                ORDER BY Jobs DESC
                """
            )
        )

    def jobs_by_role(self) -> pd.DataFrame:
        return pd.DataFrame(
            fetch_all(
                """
                SELECT title AS Role, COUNT(*) AS Jobs
                FROM jobs
                GROUP BY title
                ORDER BY Jobs DESC
                """
            )
        )

    def recent_searches(self) -> pd.DataFrame:
        return pd.DataFrame(
            fetch_all(
                """
                SELECT keyword AS Keyword, location AS Location, result_count AS Results, searched_at AS "Searched At"
                FROM searches
                ORDER BY searched_at DESC
                LIMIT 25
                """
            )
        )

    def location_chart(self, df: pd.DataFrame):
        return px.bar(df, x="Location", y="Jobs", title="Jobs by Location", text_auto=True)

    def role_chart(self, df: pd.DataFrame):
        return px.pie(df, names="Role", values="Jobs", title="Role Distribution")
