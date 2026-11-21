import { useEffect, useState } from 'react'

const ESPERA_ANTES_DO_AVISO_MS = 4000

/** Indicador de carregamento; depois de alguns segundos explica a hibernação do Render. */
export function Carregando({ texto = 'Carregando…' }: { texto?: string }) {
  const [demorando, setDemorando] = useState(false)
  useEffect(() => {
    const id = window.setTimeout(() => setDemorando(true), ESPERA_ANTES_DO_AVISO_MS)
    return () => window.clearTimeout(id)
  }, [])
  return (
    <div className="estado-vazio" role="status" aria-live="polite">
      <p>{texto}</p>
      {demorando && (
        <p className="texto-suave">
          O servidor gratuito pode estar acordando — o primeiro acesso leva cerca de 1 minuto.
        </p>
      )}
    </div>
  )
}
