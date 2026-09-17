# AI Data Analyst Frontend

The `frontend` directory contains the React + Vite user interface for the AI Data Analyst application. It lets a user submit a natural-language business question to the local FastAPI backend, inspect the generated SQL and returned data, read the AI-generated insight, view visualization output, and restore previous successful queries.

For the complete backend, database, LangGraph, and setup documentation, see the [root README](../README.md).

## Tech stack

- React 19 and React DOM
- Vite
- Tailwind CSS 4 through `@tailwindcss/vite`
- Recharts for bar-chart rendering
- `react-markdown` is present as a frontend dependency
- ESLint for frontend linting

## Features

- Natural-language question input
- Analyze Data action with loading and progress stages
- Backend-generated SQL display
- Query results table with numeric and boolean formatting
- AI analysis and final response display
- Visualization metadata and bar-chart rendering when returned by the backend
- History page with case-insensitive question search
- Row counts on history cards
- Restoration of the saved question, SQL, rows, analysis, visualization, and final response
- Clear and retry actions

## Project structure

```text
frontend/
├── public/
│   ├── favicon.svg
│   └── icons.svg
├── src/
│   ├── assets/
│   ├── App.jsx        # Main application component and UI flow
│   ├── App.css
│   ├── index.css      # Tailwind import
│   └── main.jsx       # React entry point
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
└── vite.config.js
```

The current UI is implemented in the single `App` component in `src/App.jsx`; there are no separate history or results component files.

## Installation

Install the frontend dependencies from this directory:

```bash
cd frontend
npm install
```

The backend must also be configured and running for analysis and history requests. See the [root README](../README.md).

## Available npm commands

These scripts are defined in `package.json`:

```bash
npm run dev      # Start the Vite development server
npm run build    # Create a production build in dist/
npm run lint     # Run ESLint
npm run preview  # Preview the production build locally
```

## Development server

Start Vite with:

```bash
npm run dev
```

Vite serves the application at `http://localhost:5173` by default. The current `vite.config.js` registers the React and Tailwind plugins and does not define a proxy.

## Backend API connection

`src/App.jsx` directly calls the local FastAPI server:

```text
http://127.0.0.1:8000/history
http://127.0.0.1:8000/analyze
```

The Analyze Data request is a JSON `POST`:

```json
{
  "question": "What are the top 5 products by revenue this year?"
}
```

The frontend does not read a `VITE_*` variable and does not use Axios. The backend must allow the frontend origin through CORS; the current FastAPI configuration allows the local development origins used by Vite.

## User flow

### Query input

The main page stores the textarea value in React state. Clicking **Analyze Data** rejects an empty question, clears the previous error/result state, and sends the trimmed question to `/analyze`.

### Loading and progress UI

While the request is running, the button is disabled and the UI shows six progress stages:

1. Understanding your question
2. Retrieving database schema
3. Generating SQL
4. Validating SQL query
5. Executing query
6. Analyzing results

The progress indicator is visual feedback driven by a timer; it does not receive per-stage events from the backend.

### Analysis display

The response is stored in the `result` state. The analysis panel displays `result.analysis`, falling back to `result.final_response` when analysis is empty.

### Generated SQL

The generated SQL is available in a collapsible panel using `result.sql`.

### Query results table

When rows are returned, the UI builds table headers from the first row and renders all row values. Numeric values are formatted with the `en-IN` locale and up to two fractional digits; booleans are shown as Yes/No and null values as an em dash. Empty results show a no-results message.

### Visualization

The frontend reads `result.visualization` and uses the returned `x_axis`, `y_axis`, and `title`. Recharts renders a bar chart when `chart_type` is `bar` and rows are present. Visualization metadata is still displayed for other returned chart types, but the current UI does not render line or pie chart components.

## History page

Clicking **History** switches to the history view. The page loads records from `GET /history` when the application starts and refreshes them after a successful analysis.

### History search

The search box filters the loaded history list by checking whether each question contains the search text, case-insensitively. This filtering is client-side; there is no separate search API request.

### Restoring previous queries

Each history card receives the complete record from `/history`. Selecting a card places these fields into the same result state used by a new analysis:

```text
question
generated_sql → sql
result_rows   → rows
analysis
visualization
final_response
```

The main result panels then render the restored table, analysis, SQL, and visualization without executing the query again. The current backend returns up to 50 newest records and there is no separate query-detail endpoint.

## Production build

Build the frontend with:

```bash
npm run build
```

Vite writes the production assets to `frontend/dist/`. To preview that build locally:

```bash
npm run preview
```

The build still expects the backend API at the hard-coded local URL in `src/App.jsx`; no deployment URL configuration is implemented.

## Environment and security notes

The frontend has no environment file or runtime configuration. The API URL is currently in the React source, and the browser sends questions directly to the local backend.

There is no authentication, authorization, user/session management, or frontend secret storage implemented. Do not place API keys or database credentials in this frontend directory. Gemini and PostgreSQL configuration belongs to the backend `.env` file described in the root README.

## Related documentation

See the [root README](../README.md) for backend installation, PostgreSQL and Alembic setup, seed data, LangGraph workflow, API routes, and project architecture.
