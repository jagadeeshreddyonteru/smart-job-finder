from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    company_name: str
    website: str
    careers_page: str
    location: str
    industry: str
    public_hr_email: str | None = None
