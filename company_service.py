from __future__ import annotations

from database.db import execute, fetch_all, init_db
from models.company import Company


SEED_COMPANIES: list[Company] = [
    Company("TCS", "https://www.tcs.com", "https://www.tcs.com/careers", "Hyderabad", "IT Services", "careers@tcs.com"),
    Company("Infosys", "https://www.infosys.com", "https://www.infosys.com/careers", "Hyderabad", "IT Services", "askus@infosys.com"),
    Company("Wipro", "https://www.wipro.com", "https://careers.wipro.com", "Hyderabad", "IT Services", None),
    Company("Deloitte", "https://www.deloitte.com", "https://www.deloitte.com/global/en/careers.html", "Hyderabad", "Consulting", None),
    Company("Accenture", "https://www.accenture.com", "https://www.accenture.com/in-en/careers", "Bangalore", "Consulting", None),
    Company("Capgemini", "https://www.capgemini.com", "https://www.capgemini.com/careers", "Bangalore", "IT Services", None),
    Company("Zoho", "https://www.zoho.com", "https://www.zoho.com/careers", "Chennai", "Product", "careers@zohocorp.com"),
    Company("Freshworks", "https://www.freshworks.com", "https://www.freshworks.com/company/careers", "Chennai", "SaaS", None),
    Company("Tech Mahindra", "https://www.techmahindra.com", "https://www.techmahindra.com/en-in/careers", "Pune", "IT Services", None),
    Company("HCLTech", "https://www.hcltech.com", "https://www.hcltech.com/careers", "Noida", "IT Services", None),
]


class CompanyService:
    def __init__(self) -> None:
        init_db()

    def seed_companies(self) -> None:
        for company in SEED_COMPANIES:
            execute(
                """
                INSERT OR IGNORE INTO companies
                (company_name, website, careers_page, location, industry, public_hr_email)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    company.company_name,
                    company.website,
                    company.careers_page,
                    company.location,
                    company.industry,
                    company.public_hr_email,
                ),
            )

    def list_locations(self) -> list[str]:
        self.seed_companies()
        rows = fetch_all("SELECT DISTINCT location FROM companies ORDER BY location")
        return [row["location"] for row in rows]

    def search_companies(self, location: str = "", industry: str = "") -> list[dict]:
        self.seed_companies()
        filters: list[str] = []
        params: list[str] = []

        if location:
            filters.append("LOWER(location) LIKE LOWER(?)")
            params.append(f"%{location}%")
        if industry:
            filters.append("LOWER(industry) LIKE LOWER(?)")
            params.append(f"%{industry}%")

        where = f"WHERE {' AND '.join(filters)}" if filters else ""
        return fetch_all(
            f"""
            SELECT company_id, company_name, website, careers_page, location, industry, public_hr_email
            FROM companies
            {where}
            ORDER BY company_name
            """,
            params,
        )
