import Card from "../common/Card";

// A simple wrapper so every chart looks consistent inside a card.
function ChartCard({ title, children }) {
  return (
    <Card title={title}>
      <div className="w-full h-64">{children}</div>
    </Card>
  );
}

export default ChartCard;
