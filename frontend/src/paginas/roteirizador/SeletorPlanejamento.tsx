import type { Operacao } from '../../tipos/api'
import { dataDeHoje } from '../../utilitarios/formatacao'

type Propriedades = {
  operacoes: Operacao[]
  operacaoId: number | null
  data: string
  aoMudar: (escolha: { operacaoId?: number | null; data?: string }) => void
}

/** HU-011: operação e data do planejamento. Data passada abre em modo consulta (RN-L02). */
export function SeletorPlanejamento({ operacoes, operacaoId, data, aoMudar }: Propriedades) {
  return (
    <div className="cartao barra-filtros" role="group" aria-label="Planejamento">
      <label className="campo">
        Operação
        <select
          value={operacaoId ?? ''}
          onChange={(e) => aoMudar({ operacaoId: e.target.value ? Number(e.target.value) : null })}
        >
          <option value="">Escolha a operação…</option>
          {operacoes.map((operacao) => (
            <option key={operacao.id} value={operacao.id}>
              {operacao.nome}
            </option>
          ))}
        </select>
      </label>
      <label className="campo">
        Data da rota
        <input
          type="date"
          value={data}
          required
          onChange={(e) => e.target.value && aoMudar({ data: e.target.value })}
        />
      </label>
      {data < dataDeHoje() && (
        <span className="selo selo-vencendo">Data passada: somente consulta</span>
      )}
    </div>
  )
}
