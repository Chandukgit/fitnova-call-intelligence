// A simple pulsing placeholder shown while mock data "loads".
function LoadingSkeleton({ className = "h-24 w-full" }) {
  return <div className={`animate-pulse bg-gray-100 rounded-lg ${className}`} />;
}

export default LoadingSkeleton;
