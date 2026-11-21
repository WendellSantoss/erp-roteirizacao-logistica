import { useCallback, useState } from 'react'
import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { MensagemErro } from '../../componentes/MensagemErro'
import { TituloPagina } from '../../componentes/TituloPagina'
import { useSessao } from '../../hooks/contextoSessao'
import { useConsulta } from '../../hooks/useConsulta'
import {
  consultarLimites,
  listarEquipesAtivas,
  listarSaidasDoDia,
  registrarSaida,
} from '../../servicos/almoxarifado'
import { ErroApi, mensagemDeErro, POLO_TODOS } from '../../servicos/cliente'
import type { PedidoSaidaKit } from '../../tipos/api'
import { dataDeHoje } from '../../utilitarios/formatacao'
import { DialogoBloqueio } from './DialogoBloqueio'
import { FormularioSaida } from './FormularioSaida'
import { TabelaLimites } from './TabelaLimites'
import { TabelaSaidas } from './TabelaSaidas'

const CODIGO_TRAVA = 'TRAVA_HISTORICO_KIT_EXCEDIDA'

function useRegistroDeSaida(aoRegistrar: () => void) {
  const [enviando, setEnviando] = useState(false)
  const [bloqueio, setBloqueio] = useState('')
  const [erro, setErro] = useState('')
  const [sucesso, setSucesso] = useState('')

  const registrar = async (pedido: PedidoSaidaKit) => {
    setEnviando(true)
    setErro('')
    setSucesso('')
    try {
      await registrarSaida(pedido)
      setSucesso('Saída registrada.')
      return true
    } catch (falha) {
      if (falha instanceof ErroApi && falha.codigo === CODIGO_TRAVA) setBloqueio(falha.message)
      else setErro(mensagemDeErro(falha))
      return false
    } finally {
      setEnviando(false)
      aoRegistrar()
    }
  }
  return { enviando, bloqueio, erro, sucesso, registrar, fecharBloqueio: () => setBloqueio('') }
}

function LimitesEFormulario({ podeRegistrar }: { podeRegistrar: boolean }) {
  const carregarLimites = useCallback(() => consultarLimites(), [])
  const carregarEquipes = useCallback(() => listarEquipesAtivas(), [])
  const carregarSaidas = useCallback(() => listarSaidasDoDia(dataDeHoje()), [])
  const limites = useConsulta(carregarLimites)
  const equipes = useConsulta(carregarEquipes)
  const saidas = useConsulta(carregarSaidas)
  const registro = useRegistroDeSaida(() => {
    limites.recarregar()
    saidas.recarregar()
  })

  return (
    <>
      <EstadoDaConsulta consulta={limites}>
        {(dados) => <TabelaLimites kits={dados.kits} />}
      </EstadoDaConsulta>
      {podeRegistrar && limites.dados && equipes.dados && (
        <FormularioSaida
          equipes={equipes.dados.resultados}
          kits={limites.dados.kits}
          enviando={registro.enviando}
          aoRegistrar={registro.registrar}
        />
      )}
      {registro.sucesso && (
        <div className="aviso aviso-info" role="status">
          {registro.sucesso}
        </div>
      )}
      {registro.erro && <MensagemErro mensagem={registro.erro} />}
      <h2>Saídas de hoje</h2>
      <EstadoDaConsulta consulta={saidas}>
        {(dados) => <TabelaSaidas saidas={dados.resultados} />}
      </EstadoDaConsulta>
      {registro.bloqueio && (
        <DialogoBloqueio mensagem={registro.bloqueio} aoFechar={registro.fecharBloqueio} />
      )}
    </>
  )
}

/** HU-016: saída de kits com trava de histórico. */
export function PaginaAlmoxarifado() {
  const { polo, podeEditar } = useSessao()
  return (
    <>
      <TituloPagina
        titulo="Almoxarifado"
        subtitulo="Saída de kits limitada ao que foi executado no dia anterior (trava de histórico)."
      />
      {polo === POLO_TODOS ? (
        <div className="aviso aviso-info">
          Selecione um polo no cabeçalho: o limite de kits é calculado por polo.
        </div>
      ) : (
        <LimitesEFormulario podeRegistrar={podeEditar('almoxarifado')} />
      )}
    </>
  )
}
