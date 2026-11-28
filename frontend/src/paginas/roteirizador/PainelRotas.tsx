import { ListaVazia } from '../../componentes/ListaVazia'
import type { Planejamento } from '../../tipos/api'
import { formatarDataHora } from '../../utilitarios/formatacao'

const ROTULO_STATUS = { ABERTO: 'Em aberto', FINALIZADO: 'Finalizado', DESPACHADO: 'Despachado' }

type Propriedades = {
  painel: Planejamento
  podeEditar: boolean
  ocupado: boolean
  aoFinalizar: () => void
  aoGerarRpa: () => void
}

function AcoesDoPlanejamento({
  painel,
  podeEditar,
  ocupado,
  aoFinalizar,
  aoGerarRpa,
}: Propriedades) {
  const { status, arquivo_rpa: arquivo } = painel.planejamento
  if (!podeEditar) return null
  return (
    <div className="barra-acoes">
      <button
        type="button"
        className="botao"
        disabled={ocupado || status !== 'ABERTO' || !painel.rotas.length}
        onClick={aoFinalizar}
      >
        Finalizar planejamento
      </button>
      <button
        type="button"
        className="botao botao-primario"
        disabled={ocupado || status === 'ABERTO'}
        onClick={aoGerarRpa}
      >
        {arquivo ? 'Baixar arquivo RPA novamente' : 'Gerar arquivo RPA'}
      </button>
    </div>
  )
}

/** Rotas do planejamento, finalização (HU-013) e arquivo RPA (HU-014). */
export function PainelRotas(props: Propriedades) {
  const { planejamento, rotas } = props.painel
  const arquivo = planejamento.arquivo_rpa
  return (
    <section className="cartao" aria-labelledby="titulo-rotas">
      <h2 id="titulo-rotas">
        Rotas · <span className="selo">{ROTULO_STATUS[planejamento.status]}</span>
      </h2>
      {rotas.length === 0 ? (
        <ListaVazia titulo="Nenhuma rota neste planejamento">
          Selecione OSs no mapa e clique em “Criar Rota”.
        </ListaVazia>
      ) : (
        <ul className="lista-rotas">
          {rotas.map((rota) => (
            <li key={rota.id}>
              <span
                className="marcador-cor"
                style={{ background: rota.cor || '#7c3aed' }}
                aria-hidden="true"
              />
              <strong>{rota.nome}</strong> · {rota.equipe.nome} ({rota.equipe.placa || 'sem placa'})
              · {rota.ordens.length} OSs · início {rota.previsao_inicio}
            </li>
          ))}
        </ul>
      )}
      {planejamento.finalizado_em && (
        <p className="texto-suave">
          Finalizado em {formatarDataHora(planejamento.finalizado_em)} por{' '}
          {planejamento.finalizado_por}
        </p>
      )}
      {arquivo && (
        <p className="texto-suave">
          Arquivo <span className="mono">{arquivo.nome_arquivo}</span> · {arquivo.total_ordens} OSs
          · hash <span className="mono">{arquivo.hash_sha256.slice(0, 12)}…</span>
        </p>
      )}
      <AcoesDoPlanejamento {...props} />
    </section>
  )
}
