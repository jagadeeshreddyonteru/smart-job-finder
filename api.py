from __future__ import annotations

from fastapi import FastAPI, Query

from services.analytics import AnalyticsService
from services.company_service import CompanyService
from services.job_service import ROLE_KEYWORDS, JobService

app = FastAPI(title="AI Job Finder API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/roles")
def roles() -> dict[str, list[str]]:
    return {"roles": ROLE_KEYWORDS}


@app.get("/companies")
def companies(location: str = "", industry: str = "") -> dict[str, list[dict]]:
    service = CompanyService()
    return {"companies": service.search_companies(location=location, industry=industry)}


@app.get("/jobs")
def jobs(
    keyword: str = Query(default="Any Job"),
    location: str = Query(default=""),
    limit: int = Query(default=100, ge=1, le=500),
) -> dict[str, list[dict]]:
    service = JobService()
    df = service.search_jobs(keyword=keyword, location=location, max_results=limit)
    return {"jobs": df.fillna("").to_dict(orient="records")}


@app.get("/analytics/summary")
def summary() -> dict[str, int]:
    return AnalyticsService().summary_metrics()
