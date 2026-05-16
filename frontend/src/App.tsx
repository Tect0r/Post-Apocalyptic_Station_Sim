import { useState } from "react";
import { getAccessToken } from "./api/apiClient";
import { AuthPage } from "./pages/AuthPage";
import { WorldObserverPage } from "./pages/WorldObserverPage";
import "./App.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(Boolean(getAccessToken()));

  if (!isAuthenticated) {
    return <AuthPage onAuthenticated={() => setIsAuthenticated(true)} />;
  }

  return <WorldObserverPage onLogout={() => setIsAuthenticated(false)} />;
}

export default App;