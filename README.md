# AI Job Finder

AI Job Finder is a Python + Streamlit application for finding companies by location, viewing role-based openings, saving searches to SQLite, analyzing job trends, and exporting results to CSV, Excel, and PDF.

The project is intentionally compliant: it stores company names, official websites, careers pages, job details, apply links, and public hiring inboxes when published by the company. It does not scrape private recruiter phone numbers, personal emails, LinkedIn profiles, or restricted job portals.

## Architecture

```text
+------------------+
| Streamlit UI     |
+------------------+
          |
          v
+------------------+
| FastAPI Backend  |
+------------------+
          |
          v
+------------------+
| Job Search Layer |
+------------------+
          |
          v
+------------------+
| SQLite Database  |
+------------------+
          |
          v
+------------------+
| Export Engine    |
+------------------+
```

## Folder Structure

```text
AI_Job_Finder/
|-- app.py
|-- api.py
|-- database/
|   |-- db.py
|   `-- schema.sql
|-- services/
|   |-- analytics.py
|   |-- company_service.py
|   |-- export_service.py
|   |-- job_service.py
|   |-- matching_service.py
|   `-- public_source_service.py
|-- models/
|   |-- company.py
|   `-- job.py
|-- pages/
|   |-- dashboard.py
|   |-- search.py
|   |-- analytics_page.py
|   `-- exports.py
|-- data/
|   `-- jobs.db
|-- exports/
|-- requirements.txt
`-- README.md
```

## Features

- Search jobs by location and role.
- Supported quick filters: Python Developer, SQL Developer, Data Analyst, MIS Executive, Customer Support, and Any Job.
- Display company, role, experience, job type, skills, public HR email, careers page, apply link, source, and posted date.
- Optional resume skill matching with a match score.
- SQLite database with companies, jobs, searches, and export history.
- Dashboard metrics and Plotly charts.
- Export results to CSV, Excel, and PDF.
- FastAPI endpoints for future frontend or mobile integrations.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the Streamlit App

```powershell
streamlit run app.py
```

Open the URL shown in the terminal, usually `http://localhost:8501`.

## Run the FastAPI Backend

```powershell
uvicorn api:app --reload
```

API docs will be available at `http://localhost:8000/docs`.

## API Endpoints

- `GET /health`
- `GET /roles`
- `GET /companies?location=Hyderabad`
- `GET /jobs?keyword=Python%20Developer&location=Hyderabad`
- `GET /analytics/summary`

## Database Design

### companies

Stores company name, website, careers page, location, industry, and public hiring email when available.

### jobs

Stores job title, location, experience, job type, apply link, source, posted date, description, and skills.

### searches

Stores keyword, location, result count, and search timestamp.

### exports

Stores export type, file path, row count, and timestamp.

## Adding Real Job Data

Use approved sources:

- Official company careers pages.
- Public RSS feeds.
- Job APIs with permission and API keys.
- Your own manually collected company list.

Avoid restricted scraping:

- Do not bypass anti-bot systems.
- Do not scrape LinkedIn, Naukri, Indeed, or similar portals without permission.
- Do not collect private recruiter phone numbers or personal emails.

The `services/public_source_service.py` file includes helpers for user-provided public pages. Keep any production integration inside that service or a new provider service.

## Deployment Guide

### GitHub

```powershell
git init
git add .
git commit -m "Initial AI Job Finder app"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

### Streamlit Community Cloud

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app from the repository.
4. Set the entry point to `app.py`.
5. Deploy.

### Render or Railway for FastAPI

Use this start command:

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

For persistent production data, replace SQLite with PostgreSQL and set the connection string through environment variables.

## Resume Project Title

AI-Powered Location-Based Job Finder

## Resume Description

Developed a Python application using Streamlit, FastAPI, SQLite, Pandas, and Plotly to search job openings by role and location, manage company career data, calculate resume-to-job match scores, visualize hiring trends, and export reports to Excel, CSV, and PDF.
