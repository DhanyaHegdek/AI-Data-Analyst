import { useState } from "react";
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
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
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

                <YAxis />

                <Tooltip />

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

          <div className="flex items-center gap-2 text-sm text-slate-300">
            <span className="h-2.5 w-2.5 rounded-full bg-green-400" />
            API Connected
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-12">
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

            <div className="mt-4 flex justify-end">
              <button
                type="button"
                onClick={analyzeData}
                disabled={loading}
                className="rounded-xl bg-indigo-600 px-6 py-3 font-medium transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Analyzing..." : "Analyze Data →"}
              </button>
            </div>
          </div>
        </section>

        {error && (
          <section className="mx-auto mt-6 max-w-4xl">
            <div className="rounded-xl border border-red-900 bg-red-950/40 p-4 text-red-300">
              {error}
            </div>
          </section>
        )}

        {result && (
          <section className="mx-auto mt-8 max-w-4xl space-y-6">
            {/* Analysis */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="mb-4 text-lg font-semibold">
                🤖 Analysis
              </h3>

              <p className="whitespace-pre-line text-slate-300">
                {result.final_response}
              </p>
            </div>

            {/* SQL */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="mb-4 text-lg font-semibold">
                🔍 Generated SQL
              </h3>

              <pre className="overflow-x-auto rounded-xl bg-slate-950 p-4 text-sm text-slate-300">
                {result.sql}
              </pre>
            </div>

            {/* Query Results */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="mb-4 text-lg font-semibold">
                📊 Query Results
              </h3>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-slate-700">
                      {result.rows?.[0] &&
                        Object.keys(result.rows[0]).map((key) => (
                          <th
                            key={key}
                            className="px-4 py-3 text-slate-400"
                          >
                            {key}
                          </th>
                        ))}
                    </tr>
                  </thead>

                  <tbody>
                    {result.rows?.map((row, index) => (
                      <tr
                        key={index}
                        className="border-b border-slate-800"
                      >
                        {Object.values(row).map((value, valueIndex) => (
                          <td
                            key={valueIndex}
                            className="px-4 py-3 text-slate-300"
                          >
                            {value}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Visualization */}
            {renderVisualization()}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;