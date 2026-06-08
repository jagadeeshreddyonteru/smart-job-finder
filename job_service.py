from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from database.db import execute, fetch_all, init_db
from services.company_service import CompanyService


ROLE_KEYWORDS = [
    "Python Developer",
    "SQL Developer",
    "Data Analyst",
    "MIS Executive",
    "Customer Support",
    "Any Job",
]

SEED_JOB_TEMPLATES = [
    ("Python Developer", "0-2 Years", "Full Time", "Python, FastAPI, SQL, Git", "Build backend APIs and automate data workflows."),
    ("SQL Developer", "1-3 Years", "Full Time", "SQL, Stored Procedures, ETL, Excel", "Write optimized queries and maintain reporting datasets."),
    ("Data Analyst", "0-3 Years", "Full Time", "Python, SQL, Power BI, Statistics", "Analyze business data and build dashboards for operations teams."),
    ("MIS Executive", "0-2 Years", "Full Time", "Excel, SQL, Reporting, VBA", "Prepare daily MIS reports and support process automation."),
    ("Customer Support", "0-2 Years", "Rotational Shift", "Communication, CRM, Excel", "Resolve customer issues and maintain ticket quality."),
]


class JobService:
    def __init__(self) -> None:
        init_db()
        self.company_service = CompanyService()

    def seed_jobs(self) -> None:
        self.company_service.seed_companies()
        companies = fetch_all("SELECT company_id, company_name, careers_page, location FROM companies")
        for company in companies:
            for idx, template in enumerate(SEED_JOB_TEMPLATES):
                title, experience, job_type, skills, description = template
                posted = (date.today() - timedelta(days=(idx * 3) + (company["company_id"] % 5))).isoformat()
                apply_link = f"{company['careers_page']}?q={title.replace(' ', '+')}"
                execute(
                    """
                    INSERT OR IGNORE INTO jobs
                    (company_id, title, location, experience, job_type, apply_link, source, posted_date, description, skills)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        company["company_id"],
                        title,
                        company["location"],
                        experience,
                        job_type,
                        apply_link,
                        "Seeded official careers link",
                        posted,
                        description,
                        skills,
                    ),
                )

    def search_jobs(self, keyword: str = "Any Job", location: str = "", max_results: int = 200) -> pd.DataFrame:
        self.seed_jobs()
        keyword = (keyword or "Any Job").strip()
        location = (location or "").strip()

        filters: list[str] = []
        params: list[object] = []

        if keyword and keyword.lower() != "any job":
            filters.append(
                """
                (
                    LOWER(j.title) LIKE LOWER(?)
                    OR LOWER(j.skills) LIKE LOWER(?)
                    OR LOWER(j.description) LIKE LOWER(?)
                )
                """
            )
            like_keyword = f"%{keyword}%"
            params.extend([like_keyword, like_keyword, like_keyword])

        if location:
            filters.append("LOWER(j.location) LIKE LOWER(?)")
            params.append(f"%{location}%")

        where = f"WHERE {' AND '.join(filters)}" if filters else ""
        params.append(max_results)

        rows = fetch_all(
            f"""
            SELECT
                c.company_name AS Company,
                j.title AS "Job Role",
                j.location AS Location,
                j.experience AS Experience,
                j.job_type AS "Job Type",
                j.skills AS Skills,
                c.public_hr_email AS "Public HR Email",
                j.apply_link AS "Apply Link",
                c.careers_page AS "Careers Page",
                j.source AS Source,
                j.posted_date AS "Posted Date"
            FROM jobs j
            JOIN companies c ON c.company_id = j.company_id
            {where}
            ORDER BY j.posted_date DESC, c.company_name
            LIMIT ?
            """,
            params,
        )

        df = pd.DataFrame(rows)
        self.save_search(keyword, location, len(df))
        return df

    def save_search(self, keyword: str, location: str, result_count: int) -> None:
        execute(
            "INSERT INTO searches (keyword, location, result_count) VALUES (?, ?, ?)",
            (keyword, location, result_count),
        )

    def get_job_by_id(self, job_id: int) -> dict | None:
        rows = fetch_all(
            """
            SELECT j.*, c.company_name, c.website, c.careers_page, c.public_hr_email
            FROM jobs j
            JOIN companies c ON c.company_id = j.company_id
            WHERE j.job_id = ?
            """,
            (job_id,),
        )
        return rows[0] if rows else None
