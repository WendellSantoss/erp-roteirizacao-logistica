import type { OrdemServico } from '../../tipos/api'
import { formatarCoordenada, formatarDataHora, formatarHoras } from '../../utilitarios/formatacao'
import { SeloAtraso } from './SeloAtraso'

export type AcoesDaLinha = {
  podeTratar: boolean
  mostrarPolo: boolean
  /** HU-060: marcação para liberar em lote; ausente quando o filtro não é "Pendente". */
  marcacao?: { estaMarcada: (id: number) => boolean; aoAlternar: (id: number) => void }
  aoAlternarPrioridade: (ordem: OrdemServico) => void
  aoDesconsiderar: (ordem: OrdemServico) => void
}

function Coordenada({ valor }: { valor: number | null }) {
  if (valor === null)
    return (
      <span className="sem-coordenada" title="Unidade sem coordenada">
        —
      </span>
    )
  return <span className="mono">{formatarCoordenada(valor)}</span>
}

function BotoesDeTratamento({ ordem, acoes }: { ordem: OrdemServico; acoes: AcoesDaLinha }) {
  if (!acoes.podeTratar || ordem.desconsiderada) return null
  return (
    <span style={{ display: 'flex', gap: 6 }}>
      <button
        type="button"
        className="botao botao-pequeno"
        onClick={() => acoes.aoAlternarPrioridade(ordem)}
      >
        {ordem.prioridade ? 'Tirar prioridade' : 'Priorizar'}
        <span className="oculto-visualmente"> OS {ordem.numero}</span>
      </button>
      <button
        type="button"
        className="botao botao-pequeno botao-perigo"
        onClick={() => acoes.aoDesconsiderar(ordem)}
      >
        Desconsiderar<span className="oculto-visualmente"> OS {ordem.numero}</span>
      </button>
    </span>
  )
}

/** Uma linha com as colunas da HU-007, na ordem definida. */
export function LinhaOrdemServico({ ordem, acoes }: { ordem: OrdemServico; acoes: AcoesDaLinha }) {
  return (
    <tr className={ordem.em_atraso ? 'linha-atrasada' : undefined}>
      {acoes.marcacao && (
        <td>
          <input
            type="checkbox"
            aria-label={`Marcar OS ${ordem.numero}`}
            checked={acoes.marcacao.estaMarcada(ordem.id)}
            onChange={() => acoes.marcacao?.aoAlternar(ordem.id)}
          />
        </td>
      )}
      <th scope="row" className="coluna-fixa mono">
        {ordem.numero}
      </th>
      {acoes.mostrarPolo && <td>{ordem.polo.nome}</td>}
      <td>{ordem.especificacao}</td>
      <td>{ordem.tipo}</td>
      <td className="mono">{ordem.numero_imovel}</td>
      <td>{ordem.unidade.nome}</td>
      <td>{ordem.cidade}</td>
      <td className="mono">{ordem.setor}</td>
      <td className="mono">{ordem.quadra}</td>
      <td>
        <Coordenada valor={ordem.unidade.longitude} />
      </td>
      <td>
        <Coordenada valor={ordem.unidade.latitude} />
      </td>
      <td className="mono">{ordem.prazo_horas}</td>
      <td className="mono">{formatarDataHora(ordem.abertura)}</td>
      <td className="mono">{formatarHoras(ordem.tempo_decorrido_horas)}</td>
      <td>
        <SeloAtraso ordem={ordem} />
      </td>
      <td>{ordem.equipe_id ? `Equipe ${ordem.equipe_id}` : '—'}</td>
      <td>{ordem.prioridade ? <span className="selo selo-ok">Prioritária</span> : '—'}</td>
      <td>
        <BotoesDeTratamento ordem={ordem} acoes={acoes} />
      </td>
    </tr>
  )
}
