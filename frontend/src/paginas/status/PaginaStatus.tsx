import { useCallback } from 'react'
import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { useConsulta } from '../../hooks/useConsulta'
import { consultarSaude } from '../../servicos/saude'

/** Esqueleto ambulante da Etapa 2, mantido em /status: "API OK · Banco OK". */
export function PaginaStatus() {
  const carregar = useCallback(() => consultarSaude(), [])
  const consulta = useConsulta(carregar)
  return (
    <main className="tela-login">
      <section className="cartao cartao-login" aria-labelledby="titulo-status">
        <h1 id="titulo-status">GeniOS — Status do Sistema</h1>
        <EstadoDaConsulta consulta={consulta}>
          {(saude) => (
            <p style={{ fontSize: '1.25rem', fontWeight: 700, margin: 0 }}>
              {saude.status} · {saude.database}
            </p>
          )}
        </EstadoDaConsulta>
        <a href="/">Ir para o login</a>
      </section>
    </main>
  )
}
