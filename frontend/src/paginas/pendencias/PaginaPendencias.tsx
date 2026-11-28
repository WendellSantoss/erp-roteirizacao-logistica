import { useState } from 'react'
import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { ListaVazia } from '../../componentes/ListaVazia'
import { MensagemErro } from '../../componentes/MensagemErro'
import { Paginacao } from '../../componentes/Paginacao'
import { TituloPagina } from '../../componentes/TituloPagina'
import { useSessao } from '../../hooks/contextoSessao'
import { useMarcacao } from '../../hooks/useMarcacao'
import { useOrdensServico } from '../../hooks/useOrdensServico'
import { mensagemDeErro, POLO_TODOS } from '../../servicos/cliente'
import { marcarPrioridade, TAMANHO_PAGINA } from '../../servicos/ordensServico'
import type { OrdemServico, PaginaOrdens } from '../../tipos/api'
import { DialogoDesconsiderar } from './DialogoDesconsiderar'
import { FiltrosPendencias } from './FiltrosPendencias'
import { LiberacaoEmLote } from './LiberacaoEmLote'
import { TabelaOrdensServico } from './TabelaOrdensServico'

function useAcoesPendencias(recarregar: () => void) {
  const [emDesconsideracao, setEmDesconsideracao] = useState<OrdemServico | null>(null)
  const [erroAcao, setErroAcao] = useState('')
  const alternarPrioridade = async (ordem: OrdemServico) => {
    setErroAcao('')
    try {
      await marcarPrioridade(ordem.id, !ordem.prioridade)
      recarregar()
    } catch (falha) {
      setErroAcao(mensagemDeErro(falha))
    }
  }
  const fecharDialogo = () => setEmDesconsideracao(null)
  const concluirDesconsideracao = () => {
    setEmDesconsideracao(null)
    recarregar()
  }
  return {
    emDesconsideracao,
    setEmDesconsideracao,
    erroAcao,
    alternarPrioridade,
    fecharDialogo,
    concluirDesconsideracao,
  }
}

function Vazio() {
  return (
    <ListaVazia titulo="Nenhuma pendência neste filtro">
      As OSs tratadas seguem para o Roteirizador. Para trazer novas OSs, importe a planilha do dia.
    </ListaVazia>
  )
}

/** HU-060: a marcação só existe no filtro "Pendente", que é o que pode ser liberado. */
function useLiberacao(podeLiberar: boolean, recarregar: () => void) {
  const marcacao = useMarcacao()
  const aoLiberar = () => {
    marcacao.limpar()
    recarregar()
  }
  return { marcacao, podeLiberar, aoLiberar }
}

function TotalDoFiltro({ total }: { total: number }) {
  return (
    <p className="texto-suave" aria-live="polite" style={{ margin: 0 }}>
      <strong>{total}</strong> OSs neste filtro
    </p>
  )
}

function AvisoPolo() {
  return (
    <div className="aviso aviso-info">
      Selecione um polo no cabeçalho para priorizar, desconsiderar ou liberar OSs.
    </div>
  )
}

/** HU-006/007/008 e HU-060: Gerenciar Pendências. */
export function PaginaPendencias() {
  const { polo, podeEditar } = useSessao()
  const { filtro, alterarFiltro, consulta } = useOrdensServico()
  const acoes = useAcoesPendencias(consulta.recarregar)
  const podeTratar = podeEditar('pendencias') && polo !== POLO_TODOS
  const { marcacao, podeLiberar, aoLiberar } = useLiberacao(
    podeTratar && filtro.estado === 'PENDENTE',
    consulta.recarregar,
  )

  const conteudo = (pagina: PaginaOrdens) => (
    <>
      <FiltrosPendencias
        filtro={filtro}
        contadores={pagina.contadores_por_status}
        aoMudar={alterarFiltro}
      />
      <TotalDoFiltro total={pagina.total} />
      {podeLiberar && <LiberacaoEmLote marcadas={marcacao.marcadas} aoConcluir={aoLiberar} />}
      {pagina.resultados.length === 0 ? (
        <Vazio />
      ) : (
        <TabelaOrdensServico
          ordens={pagina.resultados}
          acoes={{
            podeTratar,
            mostrarPolo: polo === POLO_TODOS,
            marcacao: podeLiberar ? marcacao : undefined,
            aoAlternarPrioridade: acoes.alternarPrioridade,
            aoDesconsiderar: acoes.setEmDesconsideracao,
          }}
        />
      )}
      <Paginacao
        pagina={filtro.page}
        total={pagina.total}
        tamanho={TAMANHO_PAGINA}
        aoMudar={(page) => alterarFiltro({ page })}
      />
    </>
  )

  return (
    <>
      <TituloPagina
        titulo="Gerenciar Pendências"
        subtitulo="OSs importadas que precisam de tratamento antes do despacho."
      />
      {podeEditar('pendencias') && polo === POLO_TODOS && <AvisoPolo />}
      {acoes.erroAcao && <MensagemErro mensagem={acoes.erroAcao} />}
      <EstadoDaConsulta consulta={consulta}>{conteudo}</EstadoDaConsulta>
      {acoes.emDesconsideracao && (
        <DialogoDesconsiderar
          ordem={acoes.emDesconsideracao}
          aoFechar={acoes.fecharDialogo}
          aoConcluir={acoes.concluirDesconsideracao}
        />
      )}
    </>
  )
}
