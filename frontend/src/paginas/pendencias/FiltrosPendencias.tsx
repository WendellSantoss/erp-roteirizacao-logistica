import { useState, type FormEvent } from 'react'
import type { EstadoOS, FiltroOrdens, PaginaOrdens } from '../../tipos/api'
import { ROTULOS_ESTADO } from '../../utilitarios/formatacao'

const ESTADOS_DAS_ABAS: EstadoOS[] = ['PENDENTE', 'APTA_A_ROTEIRIZAR', 'DESCONSIDERADA']

type Propriedades = {
  filtro: FiltroOrdens
  contadores: PaginaOrdens['contadores_por_status']
  aoMudar: (mudanca: Partial<FiltroOrdens>) => void
}

export function FiltrosPendencias({ filtro, contadores, aoMudar }: Propriedades) {
  const [busca, setBusca] = useState(filtro.busca)
  const aoBuscar = (evento: FormEvent) => {
    evento.preventDefault()
    aoMudar({ busca })
  }
  return (
    <div className="barra-filtros">
      <div className="abas" role="group" aria-label="Estado da OS">
        {ESTADOS_DAS_ABAS.map((estado) => (
          <button
            key={estado}
            type="button"
            className="botao aba"
            aria-pressed={filtro.estado === estado}
            onClick={() => aoMudar({ estado })}
          >
            {ROTULOS_ESTADO[estado]}
            <span className="contador">{contadores[estado] ?? 0}</span>
          </button>
        ))}
      </div>
      <form onSubmit={aoBuscar} className="barra-filtros" role="search">
        <label className="campo">
          Buscar OS, setor ou unidade
          <input type="search" value={busca} onChange={(e) => setBusca(e.target.value)} />
        </label>
        <button type="submit" className="botao">
          Buscar
        </button>
      </form>
      <label className="campo-linha">
        <input
          type="checkbox"
          checked={filtro.atrasada}
          onChange={(e) => aoMudar({ atrasada: e.target.checked })}
        />
        Só em atraso
      </label>
    </div>
  )
}
