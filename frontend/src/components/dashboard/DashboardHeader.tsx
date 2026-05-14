type DashboardHeaderProps = {
  tick: number;
  onRefresh: () => void;
};

export function DashboardHeader({ tick, onRefresh }: DashboardHeaderProps) {
  return (
    <section className="panel dashboard-header" id="dashboard">
      <div>
        <h1>Metro Crew Command</h1>
        <p>Current World Tick: {tick}</p>
        <p className="muted">The shared world advances by server time.</p>
      </div>

      <div className="button-row">
        <button onClick={onRefresh}>Refresh</button>
      </div>
    </section>
  );
}