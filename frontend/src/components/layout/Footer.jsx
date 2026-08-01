// Simple footer shown at the bottom of the dashboard layout.
function Footer() {
  return (
    <footer className="border-t border-[var(--color-border)] py-4 px-6 text-center text-xs text-[var(--color-text-soft)]">
      © {new Date().getFullYear()} FitNova. AI Sales Call Intelligence Platform.
    </footer>
  );
}

export default Footer;
