import { UploadCloud } from "lucide-react";

// A simple visual dropzone. Not wired to any backend yet.
function UploadDropzone() {
  return (
    <div className="border-2 border-dashed border-[var(--color-border)] rounded-xl p-8 text-center hover:border-[var(--color-primary)] transition-colors">
      <UploadCloud size={28} className="mx-auto mb-2 text-[var(--color-primary)]" />
      <p className="text-sm font-medium text-[var(--color-text)]">Drag and drop a call recording</p>
      <p className="text-xs text-[var(--color-text-soft)] mt-1">or click to browse (mock only)</p>
    </div>
  );
}

export default UploadDropzone;
