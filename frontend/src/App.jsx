import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showSql, setShowSql] = useState(false);
  const [historySearch, setHistorySearch] = useState("");
  const [history, setHistory] = useState([]);

  const [showHistoryPage, setShowHistoryPage] = useState(false);

  const loadHistory = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/history");

      if (!response.ok) {
        throw new Error("Failed to load history.");
      }

      const data = await response.json();

      setHistory(data);
    } catch (err) {
      console.error("History loading failed:", err);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const analyzeData = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question.trim() }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setResult(data);

      await loadHistory();
    } catch (err) {
      console.error("Analysis error:", err);

      if (err instanceof TypeError) {
        setError(
          "Unable to connect to the AI Data Analyst API. Please make sure the backend is running."
        );
      } else {
        setError(
          err.message || "Something went wrong while analyzing your data."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const clearAnalysis = () => {
    setQuestion("");
    setResult(null);
    setError("");
    setShowSql(false);
  };

  const renderVisualization = () => {
    if (!result?.visualization || !result?.rows?.length) {
      return null;
    }

    const visualization = result.visualization;
    const rows = result.rows;

    const xAxis = visualization.x_axis;
    const yAxis = visualization.y_axis;

    // Convert numeric values so Recharts can plot them correctly.
    const chartData = rows.map((row) => ({
      ...row,
      [yAxis]: Number(row[yAxis]),
    }));

    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="mb-6 text-lg font-semibold">
          📈 Visualization
        </h3>

        <div className="mb-6 grid gap-2 text-sm text-slate-300">
          <p>
            <span className="text-slate-500">Chart:</span>{" "}
            {visualization.chart_type}
          </p>

          <p>
            <span className="text-slate-500">X-axis:</span>{" "}
            {visualization.x_axis}
          </p>

          <p>
            <span className="text-slate-500">Y-axis:</span>{" "}
            {visualization.y_axis}
          </p>

          <p>
            <span className="text-slate-500">Title:</span>{" "}
            {visualization.title}
          </p>
        </div>

        {visualization.chart_type === "bar" && (
          <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                margin={{
                  top: 10,
                  right: 30,
                  left: 20,
                  bottom: 70,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey={xAxis}
                  angle={-25}
                  textAnchor="end"
                  interval={0}
                  height={80}
                />



                <YAxis
                  tick={{ fill: "#94a3b8", fontSize: 12 }}
                  tickFormatter={(value) =>
                    Number(value).toLocaleString("en-IN")
                  }
                />

                <Tooltip
                  cursor={{ fill: "rgba(99, 102, 241, 0.08)" }}
                  contentStyle={{
                    backgroundColor: "#0f172a",
                    border: "1px solid #334155",
                    borderRadius: "12px",
                    color: "#fff",
                  }}
                  labelStyle={{
                    color: "#cbd5e1",
                  }}
                  formatter={(value) =>
                    Number(value).toLocaleString("en-IN", {
                      maximumFractionDigits: 2,
                    })
                  }
                />

                <Bar
                  dataKey={yAxis}
                  name={yAxis}
                  fill="#6366f1"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <header className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-bold">AI Data Analyst</h1>

            <p className="text-sm text-slate-400">
              Ask questions about your business data
            </p>
          </div>

          <div className="flex items-center gap-4">
            <button
              type="button"
              onClick={() => setShowHistoryPage(true)}
              className={`rounded-lg px-4 py-2 text-sm font-medium transition ${showHistoryPage
                ? "bg-indigo-600 text-white"
                : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`}
            >
              🕘 History
            </button>

            <div className="flex items-center gap-2 text-sm text-slate-300">
              <span className="h-2.5 w-2.5 rounded-full bg-green-400" />
              API Connected
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-12">
        {showHistoryPage ? (
          <section className="mx-auto max-w-4xl">
            <div className="mb-8 flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-bold">🕘 Query History</h2>
                <p className="mt-2 text-slate-400">
                  View your previous data analysis queries.
                </p>
                <div className="mt-6">
                  <input
                    type="text"
                    placeholder="🔎 Search your previous queries..."
                    value={historySearch}
                    onChange={(e) => setHistorySearch(e.target.value)}
                    className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-indigo-500"
                  />
                </div>
              </div>

              <button
                type="button"
                onClick={() => setShowHistoryPage(false)}
                className="rounded-xl border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-300 transition hover:bg-slate-800 hover:text-white"
              >
                ← Back
              </button>
            </div>

            {history.length === 0 ? (
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-10 text-center">
                <div className="text-4xl">📭</div>
                <h3 className="mt-4 text-lg font-semibold text-slate-200">
                  No query history yet
                </h3>
                <p className="mt-2 text-sm text-slate-500">
                  Your successful analyses will appear here.
                </p>
              </div>
            ) : (
              (() => {
                const filteredHistory = history.filter((item) =>
                  item.question
                    ?.toLowerCase()
                    .includes(historySearch.toLowerCase())
                );

                if (filteredHistory.length === 0) {
                  return (
                    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-10 text-center">
                      <div className="text-4xl">🔎</div>
                      <h3 className="mt-4 text-lg font-semibold text-slate-200">
                        No matching queries
                      </h3>
                      <p className="mt-2 text-sm text-slate-500">
                        Try a different search term.
                      </p>
                    </div>
                  );
                }

                return (
                  <div className="space-y-3">
                    {filteredHistory.map((item, index) => {
                      const rowCount = item.result_rows?.length ?? 0;
                      return (
                        <button
                          key={`${item.timestamp}-${index}`}
                          type="button"
                          onClick={() => {
                            setQuestion(item.question);

                            setResult({
                              question: item.question,
                              sql: item.generated_sql,
                              rows: item.result_rows || [],
                              analysis: item.analysis,
                              visualization: item.visualization,
                              final_response: item.final_response,
                              error: null,
                            });

                            setError("");
                            setShowSql(false);
                            setShowHistoryPage(false);
                          }}
                          className="w-full rounded-2xl border border-slate-800 bg-slate-900 p-5 text-left transition hover:border-indigo-500/50 hover:bg-slate-800/70"
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="min-w-0">
                              <p className="font-medium text-slate-200">
                                {item.question}
                              </p>
                              <p className="mt-2 text-xs text-slate-500">
                                {rowCount} {rowCount === 1 ? "row" : "rows"} returned
                              </p>
                            </div>

                            <span className="shrink-0 text-xs text-slate-500">
                              {item.timestamp}
                            </span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                );
              })()
            )}
          </section>
        ) : (
          <>
            <section className="mx-auto max-w-3xl text-center">
              <div className="mb-4 inline-flex rounded-full border border-slate-700 bg-slate-900 px-4 py-2 text-sm text-slate-300">
                🤖 Powered by LangGraph + Gemini
              </div>

              <h2 className="text-4xl font-bold tracking-tight sm:text-5xl">
                Ask your data anything.
              </h2>

              <p className="mt-4 text-lg text-slate-400">
                Ask a question in natural language and let AI generate, validate,
                execute, and analyze the SQL for you.
              </p>
            </section>

            <section className="mx-auto mt-10 max-w-4xl">
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
                <label
                  htmlFor="question"
                  className="mb-3 block text-sm font-medium text-slate-300"
                >
                  Your question
                </label>

                <textarea
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Example: What are the top 5 products by revenue this year?"
                  className="min-h-32 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-500"
                />

                <div className="mt-4 flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={analyzeData}
                    disabled={loading}
                    className="rounded-xl bg-indigo-600 px-6 py-3 font-medium transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {loading ? (
                      <span className="flex items-center gap-2">
                        <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                        Analyzing...
                      </span>
                    ) : (
                      "Analyze Data →"
                    )}
                  </button>

                  <button
                    type="button"
                    onClick={clearAnalysis}
                    disabled={loading || (!question && !result && !error)}
                    className="rounded-xl border border-slate-700 bg-slate-800 px-5 py-3 font-medium text-slate-300 transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    Clear
                  </button>
                </div>
              </div>
            </section>

            {loading && (
              <section className="mx-auto mt-6 max-w-4xl">
                <div className="rounded-2xl border border-indigo-900/50 bg-indigo-950/20 p-6">
                  <div className="flex items-center gap-3">
                    <span className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-400/30 border-t-indigo-400" />
                    <div>
                      <h3 className="font-semibold text-white">
                        🤖 Analyzing your data
                      </h3>
                      <p className="mt-1 text-sm text-slate-400">
                        Understanding your question, generating SQL, and analyzing the results...
                      </p>
                    </div>
                  </div>
                </div>
              </section>
            )}

            {error && (
              <section className="mx-auto mt-6 max-w-4xl">
                <div className="rounded-2xl border border-red-900/60 bg-red-950/30 p-5">
                  <div className="flex items-start gap-3">
                    <span className="text-xl">⚠️</span>
                    <div>
                      <h3 className="font-semibold text-red-200">
                        Analysis failed
                      </h3>
                      <p className="mt-1 text-sm leading-6 text-red-300">
                        {error}
                      </p>
                      <button
                        type="button"
                        onClick={analyzeData}
                        disabled={loading}
                        className="mt-4 rounded-lg border border-red-800 bg-red-950 px-4 py-2 text-sm font-medium text-red-200 transition hover:bg-red-900 disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        Try Again
                      </button>
                    </div>
                  </div>
                </div>
              </section>
            )}

            {result && (
              <section className="mx-auto mt-8 max-w-4xl space-y-6">
                <div className="flex flex-col gap-3 rounded-xl border border-emerald-900/50 bg-emerald-950/20 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex items-center gap-2">
                    <span className="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500/20 text-sm text-emerald-400">
                      ✓
                    </span>
                    <span className="text-sm font-medium text-emerald-300">
                      Query executed successfully
                    </span>
                  </div>
                  <span className="text-sm text-slate-400">
                    {result.rows?.length ?? 0}{" "}
                    {result.rows?.length === 1 ? "row" : "rows"} returned
                  </span>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                  <h3 className="mb-4 text-lg font-semibold">🤖 Analysis</h3>
                  <div className="prose prose-invert max-w-none text-slate-300">
                    <ReactMarkdown
                      components={{
                        p: ({ children }) => (
                          <p className="mb-4 leading-7 text-slate-300">{children}</p>
                        ),
                        ol: ({ children }) => (
                          <ol className="mb-4 list-decimal space-y-2 pl-6 text-slate-300">{children}</ol>
                        ),
                        ul: ({ children }) => (
                          <ul className="mb-4 list-disc space-y-2 pl-6 text-slate-300">{children}</ul>
                        ),
                        strong: ({ children }) => (
                          <strong className="font-semibold text-white">{children}</strong>
                        ),
                      }}
                    >
                      {result.final_response}
                    </ReactMarkdown>
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                  <button
                    type="button"
                    onClick={() => setShowSql((prev) => !prev)}
                    className="flex w-full items-center justify-between text-left"
                  >
                    <div>
                      <h3 className="text-lg font-semibold">🔍 Generated SQL</h3>
                      <p className="mt-1 text-sm text-slate-500">
                        {showSql ? "Hide generated SQL" : "View generated SQL"}
                      </p>
                    </div>
                    <span className="text-xl text-slate-400">
                      {showSql ? "⌃" : "⌄"}
                    </span>
                  </button>

                  {showSql && (
                    <pre className="mt-5 overflow-x-auto rounded-xl bg-slate-950 p-4 text-sm leading-6 text-slate-300">
                      {result.sql}
                    </pre>
                  )}
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                  <h3 className="mb-4 text-lg font-semibold">📊 Query Results</h3>

                  {result.rows?.length > 0 ? (
                    <div className="overflow-x-auto">
                      <table className="w-full text-left text-sm">
                        <thead>
                          <tr className="border-b border-slate-700">
                            {result.rows?.[0] &&
                              Object.keys(result.rows[0]).map((key) => (
                                <th
                                  key={key}
                                  className="whitespace-nowrap px-4 py-3 font-medium capitalize text-slate-400"
                                >
                                  {key.replace(/_/g, " ")}
                                </th>
                              ))}
                          </tr>
                        </thead>

                        <tbody>
                          {result.rows?.map((row, index) => (
                            <tr
                              key={index}
                              className="border-b border-slate-800 transition hover:bg-slate-800/50"
                            >
                              {Object.entries(row).map(([key, value], valueIndex) => {
                                const isNumber =
                                  typeof value === "number" ||
                                  (!isNaN(value) && value !== "" && value !== null);

                                const formattedValue =
                                  isNumber && typeof value !== "boolean"
                                    ? Number(value).toLocaleString("en-IN", {
                                      maximumFractionDigits: 2,
                                    })
                                    : value;

                                return (
                                  <td
                                    key={valueIndex}
                                    className={`px-4 py-3 text-slate-300 ${isNumber ? "text-right tabular-nums" : ""
                                      }`}
                                  >
                                    {formattedValue}
                                  </td>
                                );
                              })}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-8 text-center">
                      <div className="text-3xl">📭</div>
                      <p className="mt-3 font-medium text-slate-300">
                        No results found
                      </p>
                      <p className="mt-1 text-sm text-slate-500">
                        The query executed successfully, but no matching records were found.
                      </p>
                    </div>
                  )}
                </div>

                {renderVisualization()}
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;