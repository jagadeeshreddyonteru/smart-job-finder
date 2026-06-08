from __future__ import annotations

import re

import pandas as pd


class MatchingService:
    def extract_skills(self, text: str) -> set[str]:
        tokens = re.findall(r"[A-Za-z][A-Za-z+#. ]{1,30}", text.lower())
        normalized = {token.strip() for token in tokens if len(token.strip()) > 1}
        aliases = {
            "ms excel": "excel",
            "advanced excel": "excel",
            "power bi": "power bi",
            "python": "python",
            "sql": "sql",
            "fastapi": "fastapi",
            "communication": "communication",
            "crm": "crm",
            "vba": "vba",
            "etl": "etl",
            "statistics": "statistics",
            "git": "git",
        }
        found = set()
        searchable = " ".join(normalized)
        for phrase, skill in aliases.items():
            if phrase in searchable:
                found.add(skill)
        return found

    def add_match_scores(self, df: pd.DataFrame, resume_text: str) -> pd.DataFrame:
        if df.empty or not resume_text.strip():
            return df
        resume_skills = self.extract_skills(resume_text)
        scored = df.copy()

        def score(row: pd.Series) -> int:
            job_skills = self.extract_skills(str(row.get("Skills", "")))
            if not job_skills:
                return 0
            overlap = resume_skills.intersection(job_skills)
            return round((len(overlap) / len(job_skills)) * 100)

        scored["Match Score"] = scored.apply(score, axis=1)
        return scored.sort_values("Match Score", ascending=False)
