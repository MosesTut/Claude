# Timbuktoo Backend API

FastAPI backend with PostgreSQL, Anthropic Claude AI integration, and JWT authentication.

---

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Start with Docker (Recommended)

```bash
docker-compose up -d
```

Backend will be available at `http://localhost:8000`

### 4. OR Start Manually

```bash
# Start PostgreSQL (on port 5432)

# Run database migrations
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload
```

---

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new field to users"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

---

## Development

```bash
# Run server with auto-reload
uvicorn app.main:app --reload --port 8000

# Run tests (TODO)
pytest
```

---

## Environment Variables

Required variables in `.env`:

```bash
DATABASE_URL=postgresql://timbuktoo:password@localhost:5432/timbuktoo
SECRET_KEY=your-secret-key-here
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

---

## Endpoints

### Auth
- `POST /auth/signup` - Create account
- `POST /auth/login` - Login

### Preferences
- `POST /preferences` - Save preferences
- `GET /preferences` - Get preferences

### Cities (AI)
- `GET /cities/recommendations` - Get AI city recommendations

### Itineraries (AI)
- `POST /itinerary/generate` - Generate AI itinerary
- `GET /itinerary` - List itineraries
- `GET /itinerary/{id}` - Get itinerary

### Feedback
- `POST /feedback` - Submit feedback

### User
- `GET /user/me` - Get current user
- `DELETE /user/account` - Delete account
