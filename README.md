# MatchAI - Dating Service

Dating service that uses AI to help users find better matches.

## Architecture

```plaintext
                     ┌─────────────┐
                     │   Client    │
                     └──────┬──────┘
                            │
                     ┌──────┴──────┐
                     │    Nginx    │
                     └──────┬──────┘
                            │
       ┌────────────────────┴────────────────────┐
       │                                         │
┌──────┴──────┐                           ┌──────┴──────┐
│   Frontend  │                           │   Backend   │
└──────┬──────┘                           └──────┬──────┘
       │                                         │
       │                                  ┌──────┴──────┐
       │                                  │  Database   │
       │                                  └─────────────┘
       │                                         │
┌──────┴──────┐                           ┌──────┴──────┐
│    Redis    │                           │  AI Service │
└─────────────┘                           └─────────────┘
```

## Tech Stack

- **Frontend**: React, TypeScript, Redux
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Server**: Nginx
- **Containerization**: Docker

## Prerequisites

- Docker and Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 13+

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/Undrey-ua/matchai.git
cd matchai
```


2. Set up environment variables:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Start the services:

```bash
docker-compose up
```


4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Documentation

- [API Documentation](docs/api/)
- [Architecture](docs/architecture/)
- [Deployment Guide](docs/deployment/)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.