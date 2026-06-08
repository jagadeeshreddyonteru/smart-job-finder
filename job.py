from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    company_name: str
    title: str
    location: str
    experience: str
    job_type: str
    apply_link: str
    source: str
    posted_date: str
    description: str
    skills: str
    public_hr_email: str | None = None
