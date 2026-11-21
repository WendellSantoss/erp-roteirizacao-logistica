import { useState, type FormEvent } from 'react'
import { Dialogo } from '../../componentes/Dialogo'
import { MensagemErro } from '../../componentes/MensagemErro'
import { mensagemDeErro } from '../../servicos/cliente'
import { desconsiderarOrdem } from '../../servicos/ordensServico'
import type { OrdemServico } from '../../tipos/api'

type Propriedades = { ordem: OrdemServico; aoFechar: () => void; aoConcluir: () => void }

/** Desconsiderar é terminal (RN-07): exige justificativa, que vai para a trilha de auditoria. */
export function DialogoDesconsiderar({ ordem, aoFechar, aoConcluir }: Propriedades) {
  const [justificativa, setJustificativa] = useState('')
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  const aoEnviar = async (evento: FormEvent) => {
    evento.preventDefault()
    setEnviando(true)
    try {
      await desconsiderarOrdem(ordem.id, justificativa)
      aoConcluir()
    } catch (falha) {
      setErro(mensagemDeErro(falha))
      setEnviando(false)
    }
  }

  return (
    <Dialogo titulo={`Desconsiderar OS ${ordem.numero}`} aoFechar={aoFechar}>
      <form onSubmit={aoEnviar} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <p style={{ margin: 0 }}>
          A OS sai da carteira e não volta em reimportações. Essa ação não pode ser desfeita.
        </p>
        <label className="campo">
          Justificativa (obrigatória)
          <textarea
            rows={3}
            required
            maxLength={500}
            value={justificativa}
            onChange={(e) => setJustificativa(e.target.value)}
          />
        </label>
        {erro && <MensagemErro mensagem={erro} />}
        <div className="dialogo-acoes">
          <button type="button" className="botao" onClick={aoFechar}>
            Cancelar
          </button>
          <button
            type="submit"
            className="botao botao-perigo preenchido"
            disabled={enviando || !justificativa.trim()}
          >
            {enviando ? 'Desconsiderando…' : 'Desconsiderar'}
          </button>
        </div>
      </form>
    </Dialogo>
  )
}
