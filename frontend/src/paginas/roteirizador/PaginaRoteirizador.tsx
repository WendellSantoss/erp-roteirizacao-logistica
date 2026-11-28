import { useCallback } from 'react'
import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { TituloPagina } from '../../componentes/TituloPagina'
import { useSessao } from '../../hooks/contextoSessao'
import { useConsulta } from '../../hooks/useConsulta'
import { useEscolhaPlanejamento } from '../../hooks/usePlanejamento'
import { listarEquipesAtivas } from '../../servicos/almoxarifado'
import { POLO_TODOS } from '../../servicos/cliente'
import { listarOperacoes } from '../../servicos/roteirizacao'
import { formatarData } from '../../utilitarios/formatacao'
import { PlanejamentoDoDia } from './PlanejamentoDoDia'
import { SeletorPlanejamento } from './SeletorPlanejamento'

function Conteudo() {
  const { escolha, alterar, chave } = useEscolhaPlanejamento()
  const carregarOperacoes = useCallback(() => listarOperacoes(), [])
  const carregarEquipes = useCallback(() => listarEquipesAtivas(), [])
  const operacoes = useConsulta(carregarOperacoes)
  const equipes = useConsulta(carregarEquipes)

  return (
    <EstadoDaConsulta consulta={operacoes}>
      {(dados) => {
        const operacao = dados.resultados.find((o) => o.id === escolha.operacaoId)
        return (
          <>
            <SeletorPlanejamento
              operacoes={dados.resultados}
              operacaoId={escolha.operacaoId}
              data={escolha.data}
              aoMudar={alterar}
            />
            {chave && operacao ? (
              <>
                <h2>{`${operacao.nome} · ${formatarData(escolha.data)}`}</h2>
                <PlanejamentoDoDia
                  key={`${chave.operacao_id}-${chave.data}`}
                  chave={chave}
                  equipes={equipes.dados?.resultados ?? []}
                />
              </>
            ) : (
              <div className="aviso aviso-info">Escolha a operação para ver o mapa e as rotas.</div>
            )}
          </>
        )
      }}
    </EstadoDaConsulta>
  )
}

/** HU-011/012/031/056/013/014: Despacho & Rotas › Roteirizador. */
export function PaginaRoteirizador() {
  const { polo } = useSessao()
  return (
    <>
      <TituloPagina
        titulo="Roteirizador"
        subtitulo="Selecione as OSs aptas no mapa, monte as rotas do dia e gere o despacho."
      />
      {polo === POLO_TODOS ? (
        <div className="aviso aviso-info">Selecione um polo para montar rotas.</div>
      ) : (
        <Conteudo />
      )}
    </>
  )
}
