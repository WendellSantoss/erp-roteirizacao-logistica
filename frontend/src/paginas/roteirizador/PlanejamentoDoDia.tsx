import { useState } from 'react'
import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { MensagemErro } from '../../componentes/MensagemErro'
import { useSessao } from '../../hooks/contextoSessao'
import { usePlanejamento } from '../../hooks/usePlanejamento'
import { useSelecaoOrdens, type SelecaoOrdens } from '../../hooks/useSelecaoOrdens'
import type { ChavePlanejamento, Equipe, Planejamento, Rota } from '../../tipos/api'
import type { Ponto } from '../../utilitarios/geometria'
import { BarraSelecao } from './BarraSelecao'
import { DialogoCriarRota } from './DialogoCriarRota'
import { FerramentaPoligono } from './FerramentaPoligono'
import { ListaOrdensAptas } from './ListaOrdensAptas'
import { MapaRoteirizador } from './MapaRoteirizador'
import { PainelRotas } from './PainelRotas'
import { useAcoesPlanejamento } from './useAcoesPlanejamento'

type Propriedades = { chave: ChavePlanejamento; equipes: Equipe[] }
type Acoes = ReturnType<typeof useAcoesPlanejamento>

function useDesenho(selecionar: (poligono: Ponto[]) => number) {
  const [desenhando, setDesenhando] = useState(false)
  const [vertices, setVertices] = useState<Ponto[]>([])
  const [aviso, setAviso] = useState('')
  const cancelar = () => {
    setDesenhando(false)
    setVertices([])
  }
  const concluir = () => {
    const quantidade = selecionar(vertices)
    // HU-012 CA06: polígono sem OS apta não muda a seleção.
    setAviso(quantidade ? `${quantidade} OSs dentro do polígono` : 'Nenhuma OS apta nesta área')
    cancelar()
  }
  const adicionar = (ponto: Ponto) => desenhando && setVertices((atuais) => [...atuais, ponto])
  const iniciar = () => setDesenhando(true)
  return { desenhando, vertices, aviso, iniciar, cancelar, concluir, adicionar }
}

function Avisos({ motivo, acoes }: { motivo: string; acoes: Acoes }) {
  return (
    <>
      {motivo && <div className="aviso aviso-info">{motivo}</div>}
      {acoes.sucesso && (
        <div className="aviso aviso-info" role="status">
          {acoes.sucesso}
        </div>
      )}
      {acoes.erro && <MensagemErro mensagem={acoes.erro} />}
      {acoes.inconsistencias.length > 0 && (
        <ul className="aviso aviso-erro">
          {acoes.inconsistencias.map((item) => (
            <li key={item.rota + item.motivo}>
              {item.rota}: {item.motivo}
            </li>
          ))}
        </ul>
      )}
    </>
  )
}

type PropriedadesArea = { painel: Planejamento; selecao: SelecaoOrdens; editavel: boolean }

function AreaDoMapa({ painel, selecao, editavel }: PropriedadesArea) {
  const desenho = useDesenho(selecao.selecionarPorPoligono)
  return (
    <div className="roteirizador-mapa">
      <FerramentaPoligono
        desenhando={desenho.desenhando}
        vertices={desenho.vertices.length}
        desabilitada={editavel ? '' : 'Ferramenta de polígono indisponível neste planejamento.'}
        aoIniciar={desenho.iniciar}
        aoConcluir={desenho.concluir}
        aoCancelar={desenho.cancelar}
      />
      {desenho.aviso && (
        <p className="texto-suave" role="status">
          {desenho.aviso}
        </p>
      )}
      <MapaRoteirizador
        ordensAptas={painel.ordens_aptas}
        rotas={painel.rotas}
        estaSelecionada={selecao.estaSelecionada}
        vertices={desenho.vertices}
        aoClicarNoMapa={desenho.adicionar}
      />
    </div>
  )
}

type PropriedadesLateral = PropriedadesArea & { capacidade: number; aoCriarRota: () => void }

function LateralDaSelecao({ painel, selecao, editavel, ...props }: PropriedadesLateral) {
  return (
    <div className="roteirizador-lateral">
      <BarraSelecao
        quantidade={selecao.selecionadas.length}
        capacidadeMaxima={props.capacidade}
        podeCriar={editavel}
        aoLimpar={selecao.limpar}
        aoCriarRota={props.aoCriarRota}
      />
      <ListaOrdensAptas
        ordens={painel.ordens_aptas}
        estaSelecionada={selecao.estaSelecionada}
        aoAlternar={selecao.alternar}
        somenteLeitura={!editavel}
      />
    </div>
  )
}

/** Remonta o mapa após criar rota ou mudar o status: o aviso do polígono anterior some. */
function chaveDoMapa(painel: Planejamento) {
  return `${painel.rotas.length}-${painel.planejamento.status}`
}

type PropriedadesMesa = Propriedades & { painel: Planejamento; recarregar: () => void }

function Mesa({ painel, chave, equipes, recarregar }: PropriedadesMesa) {
  const { podeEditar } = useSessao()
  const selecao = useSelecaoOrdens(painel.ordens_aptas)
  const acoes = useAcoesPlanejamento(chave, recarregar)
  const [criando, setCriando] = useState(false)
  const coordenador = podeEditar('roteirizador')
  const editavel = coordenador && !painel.planejamento.somente_leitura
  const aoCriar = (rota: Rota) => {
    setCriando(false)
    selecao.limpar()
    acoes.exibirSucesso(`Rota ${rota.nome} criada com ${rota.ordens.length} OSs`)
    recarregar()
  }
  return (
    <>
      <Avisos
        motivo={coordenador ? painel.planejamento.motivo_somente_leitura : ''}
        acoes={acoes}
      />
      <div className="roteirizador">
        <AreaDoMapa
          key={chaveDoMapa(painel)}
          painel={painel}
          selecao={selecao}
          editavel={editavel}
        />
        <LateralDaSelecao
          painel={painel}
          selecao={selecao}
          editavel={editavel}
          capacidade={Math.max(0, ...equipes.map((e) => e.capacidade_diaria))}
          aoCriarRota={() => setCriando(true)}
        />
      </div>
      <PainelRotas
        painel={painel}
        podeEditar={coordenador}
        ocupado={acoes.ocupado}
        aoFinalizar={acoes.finalizar}
        aoGerarRpa={acoes.gerarRpa}
      />
      {criando && (
        <DialogoCriarRota
          chave={chave}
          ordensIds={selecao.selecionadas}
          equipes={equipes}
          aoFechar={() => setCriando(false)}
          aoCriar={aoCriar}
        />
      )}
    </>
  )
}

/** Mapa, seleção e rotas do planejamento escolhido (polo + operação + data). */
export function PlanejamentoDoDia({ chave, equipes }: Propriedades) {
  const consulta = usePlanejamento(chave)
  return (
    <EstadoDaConsulta consulta={consulta}>
      {(painel) => (
        <Mesa painel={painel} chave={chave} equipes={equipes} recarregar={consulta.recarregar} />
      )}
    </EstadoDaConsulta>
  )
}
