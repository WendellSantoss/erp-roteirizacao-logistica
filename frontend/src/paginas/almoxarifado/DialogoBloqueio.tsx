import { Dialogo } from '../../componentes/Dialogo'

/** RF-ALM-04: explica por que a saída foi bloqueada pela trava de histórico. */
export function DialogoBloqueio({
  mensagem,
  aoFechar,
}: {
  mensagem: string
  aoFechar: () => void
}) {
  return (
    <Dialogo titulo="Saída bloqueada" aoFechar={aoFechar}>
      <div className="aviso aviso-erro">{mensagem}</div>
      <p className="texto-suave" style={{ margin: 0 }}>
        A soma das saídas do dia não pode passar do que foi executado ontem neste polo.
      </p>
      <div className="dialogo-acoes">
        <button type="button" className="botao botao-primario" onClick={aoFechar}>
          Entendi
        </button>
      </div>
    </Dialogo>
  )
}
