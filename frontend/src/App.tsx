import { useEffect, useState } from 'react'
import { consultarSaude } from './servicos/saude'

export function App() {
  const [statusTexto, setStatusTexto] = useState('Verificando API e Banco...')

  useEffect(() => {
    consultarSaude()
      .then((saude) => setStatusTexto(`${saude.status} · ${saude.database}`))
      .catch(() => {
        setStatusTexto('Erro ao conectar com a API (aguarde ~1 min se o Render hibernou)')
      })
  }, [])

  return (
    <main style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>GeniOS — Status do Sistema</h1>
      <p style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{statusTexto}</p>
    </main>
  )
}

export default App
