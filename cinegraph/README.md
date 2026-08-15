# CineGraph

A movie influence explorer using Flask, React (CDN), and Neo4j.

## Structure

cinegraph/
├── backend/
│   └── app.py
├── seed/
│   └── seed.py
├── frontend/
│   └── index.html
├── queries/
│   └── queries.cypher
├── .env.example
├── requirements.txt
└── README.md

## Setup

1. Create a Python virtual environment (recommended).
2. Install packages:

   pip install -r requirements.txt

3. Copy `.env.example` to `.env`.
4. Put your Neo4j URI, username, and password in `.env`.

IMPORTANT: Do not put your real Neo4j password in GitHub. If a real password was previously exposed, rotate it in your Neo4j provider.

## Seed database

From the project root:

   python seed/seed.py

This clears existing Neo4j data and creates the CineGraph dataset.

## Run backend

   python backend/app.py

Backend:
   http://localhost:5000

Health check:
   http://localhost:5000/api/health

## Run frontend

You can open `frontend/index.html` directly for local development, or serve the project with a simple HTTP server:

   python -m http.server 8000 --directory frontend

Then open:
   http://localhost:8000

The frontend expects the Flask backend at:
   http://localhost:5000
