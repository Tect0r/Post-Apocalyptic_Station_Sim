import type { ReactNode } from "react";

type AppLayoutProps = {
  children: ReactNode;
};

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-title">Metro Sim</div>
        <nav className="sidebar-nav">
          <a href="#dashboard">Dashboard</a>
          <a href="#crew">Crew</a>
          <a href="#stations">Stations</a>
          <a href="#routes">Routes</a>
          <a href="#actions">Actions</a>
          <a href="#events">Events</a>
        </nav>
      </aside>

      <main className="main-content">{children}</main>
    </div>
  );
}