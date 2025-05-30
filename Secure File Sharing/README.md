# Secure File Sharing System (FastAPI)

A RESTful API for secure file sharing between Ops and Client users.

## Features

- JWT-based authentication
- Email verification
- Role-based file upload/download
- Encrypted one-time download links
- SQLite database (can switch to PostgreSQL)

## Setup

```bash
git clone <repo>
cd secure-file-sharing
pip install -r requirements.txt
uvicorn main:app --reload
