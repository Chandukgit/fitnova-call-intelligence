import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import ChartCard from "./ChartCard";

// Shows how the average score has changed over the months.
function ScoreTrendChart({ data }) {
  return (
    <ChartCard title="Average Score Trend">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="month" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} domain={[50, 100]} />
          <Tooltip />
          <Line type="monotone" dataKey="avgScore" stroke="#d62828" strokeWidth={2} dot={{ r: 3 }} />
        </LineChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export default ScoreTrendChart;
