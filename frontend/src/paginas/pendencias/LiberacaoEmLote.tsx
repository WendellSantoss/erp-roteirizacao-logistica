import { useState } from 'react'
import { MensagemErro } from '../../componentes/MensagemErro'
import { mensagemDeErro } from '../../servicos/cliente'
import { liberarParaRoteirizacao } from '../../servicos/ordensServico'
import type { ResultadoLiberacao } from '../../tipos/api'

function descrever(resultado: ResultadoLiberacao): string {
  const liberadas = `${resultado.liberadas.length} OSs liberadas para roteirização.`
  if (!resultado.nao_liberadas.length) return liberadas
  // HU-060 CA02: "4 OSs não liberadas: sem coordenada" com os números.
  const numeros = resultado.nao_liberadas.map((o) => `${o.numero} (${o.motivo})`).join(', ')
  return `${liberadas} ${resultado.nao_liberadas.length} OSs não liberadas: ${numeros}`
}

type Propriedades = { marcadas: number[]; aoConcluir: () => void }

/** HU-060: botão "Liberar para roteirização" das OSs marcadas na lista. */
export function LiberacaoEmLote({ marcadas, aoConcluir }: Propriedades) {
  const [enviando, setEnviando] = useState(false)
  const [mensagem, setMensagem] = useState('')
  const [erro, setErro] = useState('')
  const liberar = async () => {
    setEnviando(true)
    setErro('')
    try {
      setMensagem(descrever(await liberarParaRoteirizacao(marcadas)))
      aoConcluir()
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }
  return (
    <div className="barra-acoes">
      <button
        type="button"
        className="botao botao-primario"
        disabled={!marcadas.length || enviando}
        onClick={liberar}
      >
        {enviando ? 'Liberando…' : `Liberar para roteirização (${marcadas.length})`}
      </button>
      {mensagem && (
        <span className="aviso aviso-info" role="status">
          {mensagem}
        </span>
      )}
      {erro && <MensagemErro mensagem={erro} />}
    </div>
  )
}
