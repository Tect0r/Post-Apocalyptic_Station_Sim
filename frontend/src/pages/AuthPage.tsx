import { useState } from "react";
import { loginUser, registerUser } from "../api/authApi";

type AuthPageProps = {
  onAuthenticated: () => void;
};

export function AuthPage({ onAuthenticated }: AuthPageProps) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("test@example.com");
  const [username, setUsername] = useState("TestPlayer");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    setError(null);

    try {
      if (mode === "register") {
        await registerUser({ email, username, password });
      }

      await loginUser({ email, password });
      onAuthenticated();
    } catch (error) {
      setError(error instanceof Error ? error.message : "Authentication failed");
    }
  }

  return (
    <main className="auth-page">
      <section className="panel auth-panel">
        <h1>Metro Sim</h1>
        <p className="muted">Sign in to command your crew.</p>

        <div className="button-row">
          <button onClick={() => setMode("login")} disabled={mode === "login"}>
            Login
          </button>
          <button onClick={() => setMode("register")} disabled={mode === "register"}>
            Register
          </button>
        </div>

        <label>
          Email
          <input value={email} onChange={(event) => setEmail(event.target.value)} />
        </label>

        {mode === "register" && (
          <label>
            Username
            <input value={username} onChange={(event) => setUsername(event.target.value)} />
          </label>
        )}

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>

        {error && <div className="error-banner">{error}</div>}

        <button onClick={handleSubmit}>
          {mode === "login" ? "Login" : "Register"}
        </button>
      </section>
    </main>
  );
}