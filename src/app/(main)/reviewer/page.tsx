import ReviewerShell from "./components/ReviewerShell";

function ReviewerDashboard() {
  return <main aria-label="Reviewer dashboard" />;
}

export default function ReviewerPage() {
  return (
    <ReviewerShell>
      <ReviewerDashboard />
    </ReviewerShell>
  );
}