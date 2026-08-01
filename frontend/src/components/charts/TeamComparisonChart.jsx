import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import ChartCard from "./ChartCard";

// Compares average scores across teams.
function TeamComparisonChart({ data }) {
  return (
    <ChartCard title="Team Comparison">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 12 }} />
          <YAxis type="category" dataKey="team" tick={{ fontSize: 12 }} width={60} />
          <Tooltip />
          <Bar dataKey="score" fill="#d62828" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export default TeamComparisonChart;
