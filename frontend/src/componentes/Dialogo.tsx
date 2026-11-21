import { useEffect, useId, useRef, type ReactNode } from 'react'

type Propriedades = { titulo: string; aoFechar: () => void; children: ReactNode }

/** Diálogo modal acessível: foco inicial no diálogo e Esc fecha. */
export function Dialogo({ titulo, aoFechar, children }: Propriedades) {
  const idTitulo = useId()
  const referencia = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const anterior = document.activeElement as HTMLElement | null
    referencia.current?.focus()
    const aoTeclar = (evento: KeyboardEvent) => evento.key === 'Escape' && aoFechar()
    window.addEventListener('keydown', aoTeclar)
    return () => {
      window.removeEventListener('keydown', aoTeclar)
      anterior?.focus()
    }
  }, [aoFechar])

  return (
    <div className="fundo-dialogo">
      <div
        className="dialogo"
        role="dialog"
        aria-modal="true"
        aria-labelledby={idTitulo}
        tabIndex={-1}
        ref={referencia}
      >
        <h2 id={idTitulo}>{titulo}</h2>
        {children}
      </div>
    </div>
  )
}
