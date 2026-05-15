import type { ReactNode } from "react";

type AppLayoutProps = {
  children: ReactNode;
  onLogout?: () => void;
};

export function AppLayout({ children, onLogout }: AppLayoutProps) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-title">Metro Sim</div>

        <nav className="sidebar-nav">
          <a href="#dashboard">Dashboard</a>
          <a href="#assets">Assets</a>
          <a href="#crew">Crew</a>
          <a href="#stations">Stations</a>
          <a href="#routes">Routes</a>
          <a href="#actions">Actions</a>
          <a href="#events">Events</a>
          <a href="#players">Players</a>
          <a href="#contracts">Contracts</a>
        </nav>

        {onLogout && (
          <button className="logout-button" onClick={onLogout}>
            Logout
          </button>
        )}
      </aside>

      <main className="main-content">{children}</main>
    </div>
  );
}