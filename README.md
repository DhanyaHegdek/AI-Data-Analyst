# AI Data Analyst

AI Data Analyst is a natural-language analytics application. A user asks a business question in the React interface; the FastAPI backend uses a LangGraph workflow and Gemini to interpret the question, generate and validate PostgreSQL SQL, execute the read query, analyze the returned rows, choose a visualization, and return the result to the UI.

## Features

- Natural-language questions about an e-commerce dataset
- Structured question understanding with Gemini
- Schema-aware SQL generation
- PostgreSQL SQL parsing and safety validation before execution
- Automatic SQL correction and retry when validation fails
- Database result analysis and a final business response
- Visualization selection for bar, line, pie, or table output
- Query results rendered as a table in the frontend
- PostgreSQL-backed query history with saved SQL, rows, analysis, visualization metadata, and final response
- Search and restoration of previous queries in the frontend

## Tech stack

### Backend

- Python 3.14+
- FastAPI and Uvicorn
- Pydantic
- SQLAlchemy and PostgreSQL
- Alembic
- LangChain Google GenAI and Gemini
- LangGraph
- sqlglot
- `uv` for Python dependency and environment management

### Frontend

- React 19
- Vite
- Tailwind CSS 4 with `@tailwindcss/vite`
- Recharts
- `react-markdown` dependency (present in the frontend package)

## Architecture

```text
React + Vite frontend
        │  HTTP fetch
        ▼
FastAPI + Uvicorn
        │
        ├── /health
        ├── /analyze
        └── /history
        │
        ▼
LangGraph + Gemini workflow
        │
        ├── PostgreSQL business data (validated SELECT queries)
        └── PostgreSQL query history (SQLAlchemy)
```

The frontend currently calls `http://127.0.0.1:8000` directly. Vite is configured with the React and Tailwind plugins; no Vite proxy or frontend environment variable is defined.

## LangGraph and AI workflow

The graph is compiled in `src/ai_data_analyst/agents/graph.py`:

```text
START
  │
  ▼
Understand question
  │
  ▼
Retrieve business schema
  │
  ▼
Generate PostgreSQL SQL
  │
  ▼
Validate SQL ── invalid ──► Fix SQL ──► Validate SQL
  │
  ├── retry limit reached ──► Final response
  │
  ▼
Execute SQL
  │
  ▼
Analyze results
  │
  ▼
Select visualization
  │
  ▼
Final response
  │
  ▼
END
```

The workflow state contains the question, schema, generated SQL, validation information, rows, analysis, visualization metadata, final response, errors, and retry information. The schema supplied to the agent describes the business tables and their relationships.

## Backend architecture

- `src/ai_data_analyst/main.py` creates the FastAPI application, configures CORS, runs the graph, saves successful analyses, and exposes the API routes.
- `src/ai_data_analyst/agents/` contains the LangGraph state, nodes, routing, prompts, SQL correction, and response generation.
- `src/ai_data_analyst/services/gemini.py` creates the Gemini-backed language model.
- `src/ai_data_analyst/services/sql_executor.py` validates and executes SQL through SQLAlchemy.
- `src/ai_data_analyst/services/query_history.py` saves and loads query history.
- `src/ai_data_analyst/tools/sql_validator.py` performs SQL safety checks with sqlglot.
- `src/ai_data_analyst/core/config.py` loads configuration from `.env`.

## Database architecture

SQLAlchemy models are defined in `src/ai_data_analyst/models/`. Alembic creates the schema and adds the query-result columns in the follow-up migration.

```text
customers ──────< orders ──────< order_items >────── products >────── categories
                    │
                    └──────< payments
```

### Business tables

| Table | Main fields | Relationships |
|---|---|---|
| `customers` | `id`, `name`, `email`, `city`, `created_at` | One customer has many orders |
| `categories` | `id`, `name`, `description` | One category has many products |
| `products` | `id`, `name`, `category_id`, `price`, `created_at` | Belongs to a category; appears in order items |
| `orders` | `id`, `customer_id`, `order_date`, `total_amount`, `status` | Belongs to a customer; has items and payments |
| `order_items` | `id`, `order_id`, `product_id`, `quantity`, `unit_price` | Joins orders and products |
| `payments` | `id`, `order_id`, `payment_date`, `amount`, `status` | Belongs to an order |

Foreign keys and delete behavior are defined in the models and initial migration. Product and customer/category references are restricted; order deletion cascades to its items and payments.

### Query-history table

The `queries` table stores application history separately from the business data:

| Column | Purpose |
|---|---|
| `id` | Query-history identifier |
| `question` | Original user question |
| `generated_sql` | Generated SQL text |
| `result_rows` | JSON array of result rows |
| `analysis` | AI-generated analysis |
| `visualization` | JSON visualization metadata |
| `final_response` | Final AI response |
| `created_at` | Timestamp |

Successful analyses are saved by `/analyze`. `result_rows` values are recursively converted from `Decimal` to JSON-safe numbers before persistence. `GET /history` returns the most recent 50 records, including the saved result data used by the frontend to restore a query.

## Project structure

```text
AI-Data-analyst/
├── alembic/
│   └── versions/
├── database/
│   ├── schema/test_queries.sql
│   └── seeds/
│       ├── seed.py
│       └── seed_data.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── src/ai_data_analyst/
│   ├── agents/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tests/
│   ├── tools/
│   └── main.py
├── .env.example
├── alembic.ini
├── pyproject.toml
└── uv.lock
```

## Requirements

- Python 3.14 or newer
- `uv`
- Node.js and npm
- PostgreSQL
- A Gemini API key

## Configuration

Create a local `.env` file in the repository root. Do not commit it.

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5433/ai_data_analyst
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
APP_ENV=development
```

`DATABASE_URL` and `GEMINI_API_KEY` are required by the backend. `APP_ENV` defaults to `development` when omitted. `.env.example` contains the database placeholder; the API-key placeholder above is illustrative and must be replaced locally.

## PostgreSQL setup

Create a PostgreSQL database named `ai_data_analyst`, then set its connection URL in `.env`. The example project configuration uses port `5433`; use the port on which PostgreSQL is actually running.

Install the Python environment and dependencies from the repository root:

```bash
uv sync
```

## Migrations

Apply the current schema, including the query-result columns:

```bash
uv run alembic upgrade head
```

The migration history includes the initial business/application schema and the migration that adds `result_rows`, `analysis`, `visualization`, and `final_response` to `queries`.

## Seed data

The current deterministic seed script clears and recreates business data in `database/seeds/seed.py`. It creates 25 customers, 8 categories, 40 products, 150 orders, one to four items per order, and one payment per order. It does not clear the `queries` history table.

Run it from the repository root after migrations:

```bash
uv run python database/seeds/seed.py
```

`database/seeds/seed_data.py` is also present as an alternate seed implementation with a different sample dataset. It likewise clears business tables, so review the script before using it.

## Run the backend

From the repository root:

```bash
uv run uvicorn ai_data_analyst.main:app --reload --host 127.0.0.1 --port 8000
```

The backend is available at `http://127.0.0.1:8000`. FastAPI’s interactive documentation is available at `http://127.0.0.1:8000/docs`.

## Run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite serves the development frontend at `http://localhost:5173` by default. The backend CORS configuration allows the localhost and loopback development origins on ports 5173 and 5174.

See [`frontend/README.md`](frontend/README.md) for frontend-specific details.

## API endpoints

| Method | Path | Behavior |
|---|---|---|
| `GET` | `/health` | Returns the API health status |
| `POST` | `/analyze` | Accepts `{ "question": "..." }`, runs the graph, saves successful results, and returns SQL, rows, analysis, visualization, final response, and status fields |
| `GET` | `/history` | Returns up to 50 newest query-history records, including saved result data |

There is no separate query-detail route. The history response contains the complete record needed by the current frontend to restore a selected query.

## Example workflow

For a question such as:

```text
What are the top 5 products by revenue this year?
```

the application understands the question, supplies the business schema to Gemini, generates a PostgreSQL `SELECT`, validates it, executes it against `order_items`, `products`, and `orders`, analyzes the returned rows, selects visualization metadata, generates a final response, and persists the successful result in `queries`.

## SQL generation, validation, and execution

The SQL prompt instructs Gemini to produce one PostgreSQL `SELECT` statement using only the supplied schema. Before execution, `validate_sql()`:

1. Rejects empty SQL.
2. Rejects multiple non-empty statements.
3. Parses the statement as PostgreSQL with sqlglot.
4. Rejects insert, update, delete, create, alter, drop, and truncate expressions.
5. Requires the parsed root expression to be a `SELECT`.

Invalid SQL can be sent through the graph’s SQL-fix/retry branch. Database execution runs only after validation. The repository does not implement authentication or a separate read-only database role, so those should not be assumed from the SQL validator alone.

## Query history

After a successful graph result, the backend saves the question, SQL, rows, analysis, visualization metadata, and final response. The frontend reloads `/history`, displays the records, supports case-insensitive question search, shows row counts, and restores the selected record into the same result state used by a fresh analysis.

## Visualization

Gemini returns visualization metadata with a chart type, x-axis, y-axis, and title. The current React UI renders bar charts with Recharts and displays the visualization metadata. Table-oriented results remain available through the query-results table; the UI does not currently render line or pie charts as chart components.

## Current implementation status

Implemented today:

- FastAPI API and CORS configuration
- LangGraph analysis workflow with Gemini nodes
- PostgreSQL schema, SQLAlchemy models, and Alembic migrations
- Deterministic business seed data
- SQL validation and correction/retry path
- Query result, analysis, visualization, and final-response persistence
- React query interface, loading stages, result table, bar-chart rendering, and query history
- Frontend lint and production build scripts

Not implemented in the current codebase:

- Authentication or authorization
- A separate query-detail API endpoint
- Backend pagination or configurable history limits
- Export, dashboards, or multi-user workspaces
- Docker or deployment configuration
- A comprehensive automated API/agent test suite

Reasonable future improvements include moving the backend URL into frontend configuration, adding typed API response schemas, adding tests around the graph and API, and adding authentication before exposing the service beyond local development.


