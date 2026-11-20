// Única camada que conversa com a API (AGENTS.md §2). A URL vem da variável de ambiente.
const URL_API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

export type StatusSaude = {
  status: string
  database: string
}

export async function consultarSaude(): Promise<StatusSaude> {
  const resposta = await fetch(`${URL_API}/health`)
  if (!resposta.ok) throw new Error('Falha na resposta da API')
  return resposta.json()
}
