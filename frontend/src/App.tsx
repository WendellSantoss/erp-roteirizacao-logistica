import { useEffect, useState } from "react";

export function App() {
  const [statusTexto, setStatusTexto] = useState("Verificando API e Banco...");

  useEffect(() => {
    const apiUrl = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

    fetch(`${apiUrl}/health`)
      .then(async (res) => {
        if (!res.ok) throw new Error("Falha na resposta da API");
        const data = await res.json();
        setStatusTexto(`${data.status} · ${data.database}`);
      })
      .catch(() => {
        setStatusTexto("Erro ao conectar com a API (aguarde ~1 min se o Render hibernou)");
      });
  }, []);

  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>GeniOS — Status do Sistema</h1>
      <p style={{ fontSize: "1.25rem", fontWeight: "bold" }}>{statusTexto}</p>
    </main>
  );
}

export default App;