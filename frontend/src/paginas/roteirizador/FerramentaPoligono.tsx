import { useEffect } from 'react'

type Propriedades = {
  desenhando: boolean
  vertices: number
  desabilitada: string
  aoIniciar: () => void
  aoConcluir: () => void
  aoCancelar: () => void
}

const MINIMO_VERTICES = 3

/** Controles do desenho de polígono (HU-012). Esc cancela o desenho em andamento. */
export function FerramentaPoligono(props: Propriedades) {
  const { desenhando, aoCancelar } = props
  useEffect(() => {
    if (!desenhando) return
    const aoTeclar = (evento: KeyboardEvent) => evento.key === 'Escape' && aoCancelar()
    window.addEventListener('keydown', aoTeclar)
    return () => window.removeEventListener('keydown', aoTeclar)
  }, [desenhando, aoCancelar])

  if (props.desabilitada) return <p className="texto-suave">{props.desabilitada}</p>
  if (!desenhando)
    return (
      <button type="button" className="botao" onClick={props.aoIniciar}>
        Desenhar polígono
      </button>
    )
  return (
    <div className="barra-acoes" role="group" aria-label="Desenho do polígono">
      <span aria-live="polite">
        Clique no mapa para marcar os vértices ({props.vertices} marcados).
      </span>
      <button
        type="button"
        className="botao botao-primario"
        disabled={props.vertices < MINIMO_VERTICES}
        onClick={props.aoConcluir}
      >
        Concluir polígono
      </button>
      <button type="button" className="botao" onClick={aoCancelar}>
        Cancelar
      </button>
    </div>
  )
}
