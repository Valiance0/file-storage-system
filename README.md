# File Storage Service (FSS)

A FastAPI-based file storage service with user authentication and database management.

## Prerequisites

- Python 3.8+
- PostgreSQL installed and running (download from https://www.postgresql.org/download/)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database:
   - Open your Postgres app
   - Right-click on "Databases" and select "Create"
   - Name the database `fss_db`

3. Create `.env` file in project root:
   ```
   DATABASE_URL=postgresql://postgres:password@localhost/fss_db
   STORAGE_FILE_PATH=./storage/
   ```
   - Replace `password` with your PostgreSQL password
   - Adjust host/port if needed (default: localhost:5432)

4. Run the application:
   ```bash
   uvicorn source.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Features

- User registration and authentication
- File upload and storage with deduplication
- File retrieval
- Database persistence with SQLModel

## Project Structure

- `source/` - Main application code
  - `main.py` - FastAPI application
  - `auth.py` - Authentication logic
  - `database.py` - Database configuration
  - `schema.py` - SQLModel schemas
  - `file_utils.py` - File handling utilities
- `storage/` - File storage directory
