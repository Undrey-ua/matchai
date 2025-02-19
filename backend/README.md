# MatchAI Backend

Dating service that uses AI to analyze social media data and match users based on their interests and behavior.

## Project Structure 

backend/

├── alembic.ini # Database migration configuration
├── app/
│ ├── api/ # API endpoints
│ ├── core/ # Core functionality
│ ├── db/ # Database session and configuration
│ ├── models/ # SQLAlchemy models
│ └── schemas/ # Pydantic models
├── docs/ # Documentation
└── migrations/ # Database migrations

## Features
- User registration and authentication
- Social media data collection
- AI-based interest analysis
- User matching based on interests
- User interaction tracking

## Database
See [Database Documentation](docs/database.md) for detailed database structure.

## Setup
1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up the database:
```bash
alembic upgrade head
```

3. Run the server:
```bash
uvicorn app.main:app --reload --port 8001
```

## API Documentation
Available at http://localhost:8001/docs when server is running.
