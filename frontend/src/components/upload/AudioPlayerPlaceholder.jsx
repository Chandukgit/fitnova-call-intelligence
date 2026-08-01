import { Play } from "lucide-react";
import Card from "../common/Card";

// A visual placeholder for a real audio player.
// The actual player will be wired up once the backend provides audio files.
function AudioPlayerPlaceholder({ duration = "00:00" }) {
  return (
    <Card>
      <div className="flex items-center gap-4">
        <button className="w-10 h-10 rounded-full bg-[var(--color-primary)] flex items-center justify-center text-white">
          <Play size={16} />
        </button>

        <div className="flex-1">
          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
            <div className="h-full w-1/3 bg-[var(--color-primary)]" />
          </div>
        </div>

        <span className="text-xs text-[var(--color-text-soft)]">{duration}</span>
      </div>
    </Card>
  );
}

export default AudioPlayerPlaceholder;
