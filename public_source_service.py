from __future__ import annotations

import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class PublicSourceService:
    """Small helper for approved public career pages.

    Many job portals restrict scraping. This helper is intentionally limited to
    public company pages provided by the user or stored in the database.
    """

    def discover_public_emails(self, url: str, timeout: int = 8) -> list[str]:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "AIJobFinder/1.0"})
        response.raise_for_status()
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", response.text)
        return sorted({email for email in emails if not email.lower().startswith(("noreply@", "no-reply@"))})

    def discover_career_links(self, website: str, timeout: int = 8) -> list[str]:
        response = requests.get(website, timeout=timeout, headers={"User-Agent": "AIJobFinder/1.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        for anchor in soup.find_all("a", href=True):
            label = anchor.get_text(" ", strip=True).lower()
            href = anchor["href"].lower()
            if "career" in label or "jobs" in label or "career" in href or "jobs" in href:
                links.append(urljoin(website, anchor["href"]))
        return sorted(set(links))[:10]
