import { useState } from 'react'
import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { ListaVazia } from '../../componentes/ListaVazia'
import { MensagemErro } from '../../componentes/MensagemErro'
import { Paginacao } from '../../componentes/Paginacao'
import { TituloPagina } from '../../componentes/TituloPagina'
import { useSessao } from '../../hooks/contextoSessao'
import { useOrdensServico } from '../../hooks/useOrdensServico'
import { mensagemDeErro, POLO_TODOS } from '../../servicos/cliente'
import { marcarPrioridade, TAMANHO_PAGINA } from '../../servicos/ordensServico'
import type { OrdemServico, PaginaOrdens } from '../../tipos/api'
import { DialogoDesconsiderar } from './DialogoDesconsiderar'
import { FiltrosPendencias } from './FiltrosPendencias'
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

/** HU-006/007/008: Gerenciar Pendências. */
export function PaginaPendencias() {
  const { polo, podeEditar } = useSessao()
  const { filtro, alterarFiltro, consulta } = useOrdensServico()
  const acoes = useAcoesPendencias(consulta.recarregar)
  const podeTratar = podeEditar('pendencias') && polo !== POLO_TODOS

  const conteudo = (pagina: PaginaOrdens) => (
    <>
      <FiltrosPendencias
        filtro={filtro}
        contadores={pagina.contadores_por_status}
        aoMudar={alterarFiltro}
      />
      <p className="texto-suave" aria-live="polite" style={{ margin: 0 }}>
        <strong>{pagina.total}</strong> OSs neste filtro
      </p>
      {pagina.resultados.length === 0 ? (
        <Vazio />
      ) : (
        <TabelaOrdensServico
          ordens={pagina.resultados}
          acoes={{
            podeTratar,
            mostrarPolo: polo === POLO_TODOS,
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
      {podeEditar('pendencias') && polo === POLO_TODOS && (
        <div className="aviso aviso-info">
          Selecione um polo no cabeçalho para priorizar ou desconsiderar OSs.
        </div>
      )}
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
