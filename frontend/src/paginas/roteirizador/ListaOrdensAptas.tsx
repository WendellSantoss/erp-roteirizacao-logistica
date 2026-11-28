import { ListaVazia } from '../../componentes/ListaVazia'
import type { OrdemNoMapa } from '../../tipos/api'

type Propriedades = {
  ordens: OrdemNoMapa[]
  estaSelecionada: (id: number) => boolean
  aoAlternar: (id: number) => void
  somenteLeitura: boolean
}

/** Alternativa ao mapa operável por teclado; também remove uma OS da seleção (HU-012 CA05). */
export function ListaOrdensAptas({
  ordens,
  estaSelecionada,
  aoAlternar,
  somenteLeitura,
}: Propriedades) {
  if (!ordens.length)
    return (
      <ListaVazia titulo="Nenhuma OS apta neste polo">
        Libere OSs tratadas na tela de Pendências para que apareçam aqui.
      </ListaVazia>
    )
  return (
    <fieldset className="cartao lista-aptas" disabled={somenteLeitura}>
      <legend>OSs aptas ({ordens.length})</legend>
      <ul>
        {ordens.map((ordem) => (
          <li key={ordem.id}>
            <label>
              <input
                type="checkbox"
                checked={estaSelecionada(ordem.id)}
                onChange={() => aoAlternar(ordem.id)}
              />
              <span className="mono">{ordem.numero}</span> · {ordem.unidade.nome}
              {ordem.prioridade && <span className="selo selo-ok">Prioritária</span>}
              <br />
              <small className="texto-suave">{ordem.especificacao}</small>
            </label>
          </li>
        ))}
      </ul>
    </fieldset>
  )
}
