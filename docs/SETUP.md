# Setup

Clone the repository:

```bash
git clone https://github.com/your-repo/your-project.git
```

Create environment files:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Install dependencies:

```bash
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

Build and start containers:

```bash
docker compose up --build
```

## Container Structure

- Frontend: React application
- Backend: FastAPI application
- Database: PostgreSQL
- Cache: Redis
- Web Server: Nginx
- Container Orchestration: Kubernetes

Access container logs:

```bash
docker-compose logs -f [service_name]
```
