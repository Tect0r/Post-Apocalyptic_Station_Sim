type DashboardHeaderProps = {
  tick: number;
  onRefresh: () => void;
  onAdvanceTick: () => void;
};

export function DashboardHeader({ tick, onRefresh, onAdvanceTick }: DashboardHeaderProps) {
  return (
    <section className="panel dashboard-header" id="dashboard">
      <div>
        <h1>Metro Crew Command</h1>
        <p>Current World Tick: {tick}</p>
      </div>

      <div className="button-row">
        <button onClick={onRefresh}>Refresh</button>
        <button onClick={onAdvanceTick}>Advance Tick</button>
      </div>
    </section>
  );
}