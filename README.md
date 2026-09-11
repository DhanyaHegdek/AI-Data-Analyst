# AI Data Analyst 🤖📊

An AI-powered data analytics platform that converts natural-language questions into validated SQL queries and actionable insights.

> 🚧 **Project Status:** In development. The PostgreSQL business schema and SQLAlchemy/Alembic foundation are implemented. The AI agent, SQL security layer, API, frontend, visualization, testing, and deployment will be added incrementally.

## ✨ Planned Features

- 💬 Natural-language data questions
- 🧠 Gemini-powered analysis
- 🔎 Database schema retrieval
- 📝 Automatic SQL generation
- 🛡️ SQL validation and security
- 🗄️ Read-only PostgreSQL analysis
- 📊 Tables and charts
- ⚡ FastAPI backend
- 🕸️ LangGraph multi-node AI workflow
- ⚛️ React + Tailwind frontend
- 🧾 Query history and application metadata
- 🧪 Automated testing
- 🐳 Docker support
- 🚀 Deployment-ready architecture

## 🏗️ Architecture

```text
React + Tailwind Frontend
          │
          ▼
       FastAPI
          │
          ▼
   LangGraph + Gemini
          │
          ├── Understand Question
          ├── Schema Retrieval
          ├── SQL Generation
          ├── SQL Validation
          ├── Execute SQL
          ├── Analyze Results
          ├── Visualization
          └── Final Response
          │
          ▼
      PostgreSQL
```

## 🧠 AI Workflow

The planned agent uses a controlled multi-step workflow rather than directly executing LLM-generated SQL.

```text
START
  ↓
Question Understanding
  ↓
Schema Retrieval
  ↓
SQL Generation
  ↓
SQL Validation
  ├── Invalid → correction/retry
  ↓
Execute SQL
  ├── Error → correction/retry
  ↓
Analyze Results
  ↓
Visualization
  ↓
Final Response
```

## 🛡️ SQL Security

Generated SQL will be validated before execution.

Planned protections include:

- Block DDL such as `CREATE`, `ALTER`, and `DROP`
- Block DML such as `INSERT`, `UPDATE`, and `DELETE`
- Read-only database credentials
- Table and column access restrictions
- Query timeouts
- Row/result limits
- Controlled SQL error handling and retry

## 🗄️ Business Database

The AI analyzes an e-commerce business database.

```text
customers
    │
    └── orders
           │
           ├── order_items ── products ── categories
           │
           └── payments
```

### Tables

| Table | Purpose |
|---|---|
| `customers` | Customer information |
| `categories` | Product categories |
| `products` | Products and prices |
| `orders` | Customer orders |
| `order_items` | Products included in orders |
| `payments` | Payment information |

Example analytical question:

> What are our top 5 products by revenue this year?

Example SQL:

```sql
SELECT
    p.name,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi
    ON p.id = oi.product_id
JOIN orders o
    ON oi.order_id = o.id
WHERE EXTRACT(YEAR FROM o.order_date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY p.id, p.name
ORDER BY revenue DESC
LIMIT 5;
```

## 🧰 Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- PostgreSQL
- LangChain
- LangGraph
- Gemini

### Frontend
- React
- Vite
- Tailwind CSS

### Data & Visualization
- PostgreSQL
- Plotly

### Development
- `uv`
- Git
- GitHub
- Docker

## 📁 Project Structure

```text
AI-Data-analyst/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── database/
│   ├── schema/
│   └── seeds/
├── docs/
├── frontend/
├── src/
│   └── ai_data_analyst/
│       ├── agents/
│       ├── api/
│       ├── core/
│       ├── database/
│       │   ├── base.py
│       │   └── connection.py
│       ├── models/
│       │   ├── category.py
│       │   ├── customer.py
│       │   ├── order.py
│       │   ├── order_item.py
│       │   ├── payment.py
│       │   └── product.py
│       ├── schemas/
│       ├── services/
│       └── tools/
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
└── uv.lock
```

## 🚀 Current Progress

### Phase 1 — Database Foundation

- [x] Project structure
- [x] Python environment with `uv`
- [x] FastAPI application
- [x] PostgreSQL database
- [x] SQLAlchemy configuration
- [x] Alembic configuration
- [x] Customer model
- [x] Category model
- [x] Product model
- [x] Order model
- [x] OrderItem model
- [x] Payment model
- [x] Initial business database migration
- [x] PostgreSQL schema verification
- [ ] Realistic seed data

### Phase 2 — Basic SQL Agent

- [ ] Gemini integration
- [ ] Natural language → SQL
- [ ] SQL execution
- [ ] Basic result analysis

### Phase 3 — LangGraph Agent

- [ ] Question understanding
- [ ] Schema retrieval
- [ ] SQL generation
- [ ] SQL validation
- [ ] SQL execution
- [ ] Result analysis
- [ ] Visualization
- [ ] Final response

### Phase 4 — SQL Validation & Security

- [ ] Read-only access
- [ ] DDL/DML blocking
- [ ] Table/column permissions
- [ ] Query timeout
- [ ] Row limits
- [ ] SQL error handling
- [ ] Retry/correction flow

### Phase 5 — FastAPI

- [ ] `/api/analyze`
- [ ] Request/response schemas
- [ ] Agent integration
- [ ] Error handling

### Phase 6 — React Frontend

- [ ] Chat interface
- [ ] SQL display
- [ ] Result table
- [ ] Loading states
- [ ] Error messages
- [ ] Query history

### Phase 7 — Visualization

- [ ] Plotly integration
- [ ] Chart generation
- [ ] Table + chart responses
- [ ] Visualization selection

### Phase 8 — Production Hardening

- [ ] Authentication
- [ ] Logging
- [ ] Query limits
- [ ] Tests
- [ ] Docker
- [ ] Architecture documentation
- [ ] Security review

### Phase 9 — Portfolio

- [ ] GitHub documentation
- [ ] Screenshots
- [ ] Architecture diagram
- [ ] Demo
- [ ] Resume project description

## ⚙️ Local Development

### Install dependencies

```bash
uv sync
```

### Configure environment

Create `.env` locally:

```env
DATABASE_URL=postgresql+psycopg://postgres:<password>@localhost:<port>/ai_data_analyst
GEMINI_API_KEY=<your-api-key>
APP_ENV=development
```

Never commit `.env`, database passwords, or API keys. Use `.env.example` as the safe template.

### Run migrations

```bash
uv run alembic upgrade head
```

### Start FastAPI

```bash
uv run uvicorn ai_data_analyst.main:app --reload
```

Interactive API documentation:

```text
/docs
```

## 🎯 Example Questions

Once the AI agent is implemented, users will be able to ask questions such as:

```text
What are our top 5 products by revenue?

Which city has the most customers?

What was our monthly revenue this year?

Which product category generates the most revenue?

How many orders were cancelled?

What is the average order value?

Which products sold the most units?
```

## 🗺️ Roadmap

```text
Database
   ↓
Basic SQL Agent
   ↓
LangGraph Agent
   ↓
SQL Validation & Security
   ↓
FastAPI
   ↓
React
   ↓
Visualization
   ↓
Production Hardening
   ↓
Portfolio / Deployment
```

The backend and AI workflow are intentionally developed before the final UI so the frontend is built around a working analytical engine.

## 📌 Project Goals

This project demonstrates practical skills in:

- Python backend development
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Generative AI
- Gemini
- LangChain
- LangGraph
- Natural-language-to-SQL systems
- SQL security and validation
- React
- Data visualization
- API design
- Production-oriented architecture

## 📄 License

This project is currently being developed as a personal portfolio project.
