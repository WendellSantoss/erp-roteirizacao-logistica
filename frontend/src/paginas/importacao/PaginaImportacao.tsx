import { useCallback, useState } from 'react'
import { MensagemErro } from '../../componentes/MensagemErro'
import { TituloPagina } from '../../componentes/TituloPagina'
import { useSessao } from '../../hooks/contextoSessao'
import { useConsulta } from '../../hooks/useConsulta'
import { mensagemDeErro, POLO_TODOS } from '../../servicos/cliente'
import { enviarPlanilha, listarImportacoes } from '../../servicos/importacoes'
import type { Importacao } from '../../tipos/api'
import { motivoDeRecusa } from '../../utilitarios/planilha'
import { AreaEnvio } from './AreaEnvio'
import { HistoricoImportacoes } from './HistoricoImportacoes'
import { ResultadoImportacao } from './ResultadoImportacao'

function useEnvioDePlanilha(aoConcluir: () => void) {
  const [enviando, setEnviando] = useState(false)
  const [erro, setErro] = useState('')
  const [resultado, setResultado] = useState<Importacao | null>(null)

  const enviar = async (arquivos: File[]) => {
    const recusa = motivoDeRecusa(arquivos)
    setErro(recusa)
    setResultado(null)
    if (recusa || arquivos.length === 0) return
    setEnviando(true)
    try {
      setResultado(await enviarPlanilha(arquivos[0]))
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
      aoConcluir()
    }
  }
  return { enviando, erro, resultado, enviar }
}

/** HU-001 a HU-004: Importação da OS diária. */
export function PaginaImportacao() {
  const { polo, usuario, podeEditar } = useSessao()
  const carregarHistorico = useCallback(() => listarImportacoes(), [])
  const historico = useConsulta(carregarHistorico)
  const envio = useEnvioDePlanilha(historico.recarregar)
  const nomePolo = usuario?.polos_autorizados.find((item) => String(item.id) === polo)?.nome ?? ''

  return (
    <>
      <TituloPagina
        titulo="Importação da OS diária"
        subtitulo="Planilha do GSAN: valida o layout, filtra o escopo e atualiza a carteira sem perder o tratamento."
      />
      {podeEditar('importacao') && (
        <AreaEnvio
          desabilitada={polo === POLO_TODOS}
          enviando={envio.enviando}
          aoEscolher={envio.enviar}
        />
      )}
      {envio.erro && <MensagemErro mensagem={envio.erro} />}
      {envio.resultado && <ResultadoImportacao importacao={envio.resultado} nomePolo={nomePolo} />}
      <HistoricoImportacoes consulta={historico} />
    </>
  )
}
