# 🤖 AI-Powered Service Desk API

An enterprise-grade, high-performance asynchronous service desk REST API built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, and **PostgreSQL**. The platform leverages **Amazon Bedrock** (via the Converse API) to automatically generate ticket descriptions and perform intelligent context-aware ticket summarization & querying across your service desk database.

---

## 🚀 Key Features

* **⚡ Async-First Architecture**: Powered by Python 3.12+, FastAPI, SQLAlchemy 2.0 (with `asyncpg`), and PostgreSQL for high throughput and low latency.
* **🤖 AWS Bedrock AI Integration**:
  * **Auto-Description Generation**: Automatically creates rich support ticket descriptions based on title, priority, and status using Bedrock LLM models.
  * **Context-Aware Ticket Summarization & Querying**: Summarizes tickets, suggests professional resolutions, and answers natural language questions about existing tickets across the database.
  * **Resilient Parsing**: Custom JSON boundary extraction and fallback mechanisms to handle diverse LLM outputs gracefully.
* **⏱️ Built-in Performance Middleware**: Automatically measures execution time and injects an `X-Response-Time` header into every HTTP response.
* **📊 Comprehensive Profiling & Load Testing**:
  * **Code Execution Profiling**: Included `profile_testing.py` utility with PostgreSQL and automatic `aiosqlite` in-memory fallback.
  * **Interactive GUI Visualizer**: Integration with `SnakeViz` for visual hotspot bottleneck analysis.
  * **Swarm Load Testing**: Pre-configured `Locust` load testing suite for live stress testing.
* **🛠️ Database Evolution**: Managed schema migrations via **Alembic**.
* **🧪 Robust Test Suite**: Unit, integration, and end-to-end (E2E) testing framework using `pytest` and `pytest-asyncio`.
* **🐳 Production Ready**: Dockerized deployment setup optimized with `uv`.

---

## 📁 Project Structure

```text
ai-service-desk/
├── alembic/                # Alembic database migrations and version scripts
├── app/
│   ├── api/                # API route definitions (Tickets, AI endpoints)
│   ├── core/               # App configuration, database setup, exceptions, dependencies
│   ├── middleware/         # Custom HTTP middleware (Response time tracker)
│   ├── models/             # SQLAlchemy ORM models (Ticket, Enums)
│   ├── repositories/       # Data access layer (TicketRepository)
│   ├── schemas/            # Pydantic request/response schemas
│   ├── service/            # Business logic & AWS Bedrock integration services
│   └── main.py             # FastAPI entrypoint and lifespan context
├── test/
│   ├── unit_test/          # Service & logic unit tests
│   ├── integration_test/   # Database & route integration tests
│   ├── end_to_end_test/    # Workflow E2E tests
│   └── conftest.py         # Shared Pytest fixtures
├── Dockerfile              # Production Multi-Stage Dockerfile
├── locust.py               # Locust load testing script
├── profile_testing.py      # Automated cProfile testing & benchmark runner
├── pyproject.toml          # Project dependencies (managed via uv)
└── README.md               # Project documentation
```

---

## 🛠️ Prerequisites & Installation

### 1. Environment Setup

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/ticketdb
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=your-bedrock-model-id-or-inference-profile
```

### 2. Dependency Management (`uv`)

This project uses `uv` for ultra-fast dependency management:

```bash
# Install dependencies and sync virtual environment
uv sync
```

### 3. Database Migrations

Apply Alembic migrations to initialize the PostgreSQL schema:

```bash
uv run alembic upgrade head
```

### 4. Running the Server

Start the development server with live-reloading:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive API documentation:
* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔌 API Reference

### System Health & Status

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Returns service health and verifies active database connectivity |
| `GET` | `/ready` | Service readiness probe |

### Support Tickets (`/tickets/ticket`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/tickets/ticket` | Create a new ticket (automatically generates AI description) |
| `GET` | `/tickets/ticket` | List all tickets (supports filtering by `status` and `priority`) |
| `GET` | `/tickets/ticket/{id}` | Retrieve a specific ticket by UUID |
| `PUT` | `/tickets/ticket/{id}` | Update ticket details (`title`, `priority`, `status`) |
| `DELETE` | `/tickets/ticket/{id}` | Delete a ticket by UUID |

### AI Assistance (`/ai`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/ai/summarize` | Summarizes a ticket or answers questions about existing tickets |

**Sample Request (`POST /ai/summarize`):**
```json
{
  "ticket_description": "Give all the tickets now"
}
```

**Sample Response (`200 OK`):**
```json
{
  "summary": "AI Desk Response",
  "suggested_response": "Here is the summary of current tickets: \n- [High] Login Issue: User cannot login\n- [Medium] VPN Error: Connection timed out"
}
```

---

## 📊 Performance & Profile Testing

### 1. Code Profiling Script (`profile_testing.py`)

Run an automated CPU and event loop performance profiling test across all API endpoints:

```bash
uv run python profile_testing.py --iterations 50
```

* Automatically detects PostgreSQL connectivity or seamlessly falls back to an in-memory SQLite database (`aiosqlite`) if offline.
* Mocks AWS Bedrock calls to measure pure application execution time.
* Generates binary stats (`app_profile.prof`) and a text summary (`profile_summary.txt`).

### 2. Interactive GUI Profiler (`SnakeViz`)

To visualize execution hotspots and call trees in an interactive web browser interface:

```bash
# Install SnakeViz
uv pip install snakeviz

# Launch GUI viewer
uv run snakeviz app_profile.prof
```

### 3. Load Testing (`Locust`)

To run load tests and benchmark the API under high traffic:

```bash
uv run locust -f locust.py
```
Open your browser at **[http://localhost:8089](http://localhost:8089)** to set swarm rate and start live load testing.

---

## 🧪 Running Tests

Run the test suite with `pytest`:

```bash
uv run pytest
```

---

## 🐳 Docker Deployment

To build and run the application inside Docker:

```bash
# Build the Docker image
docker build -t ai-service-desk:latest .

# Run the container
docker run -p 8000:8000 --env-file .env ai-service-desk:latest
```
