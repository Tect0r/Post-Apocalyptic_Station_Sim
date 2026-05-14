import { useState } from "react";
import { getAccessToken } from "./api/apiClient";
import { AuthPage } from "./pages/AuthPage";
import { DashboardPage } from "./pages/DashboardPage";
import "./App.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(Boolean(getAccessToken()));

  if (!isAuthenticated) {
    return <AuthPage onAuthenticated={() => setIsAuthenticated(true)} />;
  }

  return <DashboardPage onLogout={() => setIsAuthenticated(false)} />;
}

export default App;