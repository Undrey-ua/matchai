# MatchAI - Dating Service

Dating service that uses AI to help users find better matches.

## Architecture

```plaintext
                        ┌─────────────────────┐
                        │    Користувач       │
                        │ Пости│Лайки│Інтереси│
                        └──────────┬──────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────┐
│                     AI Аналіз                            │
│                                                          │
│    ┌───────────┐         ┌──────────┐      ┌──────────┐  │
│    │   GPT     │         │ Sentence │      │ Behavior │  │
│    │  Аналіз   │         │ Vectors  │      │ Аналіз   │  │
│    │  тексту   │         │ (384-dim)│      │ патернів │  │
│    └─────┬─────┘         └────┬─────┘      └────┬─────┘  │
│          │                    │                 │        │
└──────────┼────────────────────┼─────────────────┼────────┘
           │                    │                 │
           ▼                    ▼                 ▼
    ┌─────────────────────────────────────────────────┐
    │              База даних (PostgreSQL)            │
    │        Зберігання векторів та результатів       │
    └───────────────────────┬─────────────────────────┘
                            │
                            ▼
                ┌────────────────────┐
                │  Matching Engine   │
                │ Пошук схожих людей │
                └────────┬───────────┘
                         │
                         ▼
                ┌────────────────────┐
                │  Список матчів     │
                │  за схожістю       │
                └────────────────────┘
```

## System Components

### 1. AI Analysis
- **GPT Text Analysis**
  - Post and comment analysis
  - Key topic extraction
  - Sentiment analysis
  
- **Sentence Vectors**
  - Vector representations (384 dimensions)
  - Model: all-MiniLM-L6-v2
  - Interest and content vectorization
  
- **Behavior Analysis**
  - Activity pattern analysis
  - User interaction study
  - Behavioral profile creation

### 2. Database
- PostgreSQL for data storage
- Vector storage for fast search
- Analysis results caching

### 3. Matching Engine
- Cosine similarity for vectors
- Weighted scoring of all factors
- Result ranking

## Tech Stack

- **Frontend**: React, TypeScript, Redux
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Server**: Nginx
- **Containerization**: Docker

### Backend (FastAPI)
- Python 3.12
- FastAPI framework
- SQLAlchemy ORM
- Alembic migrations
- OpenAI GPT API
- sentence-transformers

### Database
- PostgreSQL
- Vector extensions
- Fast search indexing

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

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Setup database:
```bash
createdb matchai
alembic upgrade head
```

5. Run server:
```bash
uvicorn app.main:app --reload --port 8001
```

## API Documentation

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

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

## AI Agents

```plaintext
                                 ┌──────────────────────────┐
                                 │         USER             │
                                 │    Input & Interaction   │
                     ┌──────────►│                          │◄──────────┐
                     │           └────────────┬─────────────┘           │
                     │                        │                         │
                     │                        ▼                         │
                     │           ┌────────────────────────┐             │
                     │           │     DATA COLLECTION    │             │
                     │           │ ┌──────┐┌─────┐┌─────┐ │             │
                     │           │ │Posts ││Likes││Inter│ │             │
                     │           │ └──┬───┘└──┬──┘└──┬──┘ │             │
                     │           └─────┼───────┼─────┼────┘             │
                     │                 │       │     │                  │
                     │                 ▼       ▼     ▼                  │
┌────────────────────┴─────────────────────────────────────────────┐    │
│                           AI ANALYSIS                            │    │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐ │    │
│  │   Text Agent    │   │  Vector Agent   │   │ Behavior Agent  │ │    │
│  │  [GPT-3.5/4]    │   │   [MiniLM-L6]   │   │  [Custom ML]    │ │    │
│  │• Content→Topics │   │• Text→Vectors   │   │• Actions→Pattern│ │    │
│  │• Emotion Detect │   │• 384-dim Space  │   │• Time Analysis  │ │    │
│  │• Theme Extract  │   │• Similarity Calc│   │• User Profiling │ │    │
│  └────────┬────────┘   └────────┬────────┘   └────────┬────────┘ │    │
│           │                     │                     │          │    │
└───────────┼─────────────────────┼─────────────────────┼──────────┘    │
            │                     │                     │               │
            ▼                     ▼                     ▼               │
    ┌───────────────────────────────────────────────────────────┐       │
    │                  PostgreSQL DATABASE                      │       │
    │    [pgvector extension for vector similarity search]      │       │
    └───────────────────────────┬───────────────────────────────┘       │
                                │                                       │
                                ▼                                       │
                    ┌─────────────────────────┐                         │
                    │    MATCHING ENGINE      │                         │
                    │     [Hybrid Model]      │                         │
                    │• Cosine Similarity      │                         │
                    │• Weight Optimization    │                         │
                    │• ML-based Ranking       │                         │
                    └────────────┬────────────┘                         │
                                 │                                      │
                                 ▼                                      │
                    ┌─────────────────────────┐                         │
                    │    FINAL RESULTS        ├─────────────────────────┘
                    │  [Recommendation API]   │
                    │  Personalized Matches   │
                    └─────────────────────────┘
```