import type { ReactNode } from 'react'
import { useSessao } from '../hooks/contextoSessao'
import { iniciais, ROTULOS_PERFIL } from '../utilitarios/formatacao'
import { ITENS_MENU } from '../utilitarios/menu'
import { LinkInterno } from './LinkInterno'
import { SeletorPolo } from './SeletorPolo'

function Lateral() {
  const { podeVer } = useSessao()
  return (
    <aside className="lateral">
      <div className="marca">
        <span className="marca-simbolo" aria-hidden="true">
          G
        </span>
        <span>
          <strong>GeniOS</strong>
          <small>ERP OPERACIONAL</small>
        </span>
      </div>
      <nav aria-label="Menu principal">
        <ul className="menu">
          {ITENS_MENU.filter((item) => podeVer(item.modulo)).map((item) => (
            <li key={item.caminho}>
              <LinkInterno para={item.caminho}>{item.rotulo}</LinkInterno>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  )
}

function Cabecalho({ titulo }: { titulo: string }) {
  const { usuario, encerrar } = useSessao()
  if (!usuario) return null
  return (
    <header className="cabecalho">
      <strong>{titulo}</strong>
      <div className="cabecalho-acoes">
        <SeletorPolo />
        <div className="usuario-chip">
          <span>
            <strong>{usuario.nome}</strong>
            <br />
            <span className="texto-suave">{ROTULOS_PERFIL[usuario.perfil] ?? usuario.perfil}</span>
          </span>
          <span className="avatar" aria-hidden="true">
            {iniciais(usuario.nome)}
          </span>
        </div>
        <button type="button" className="botao botao-pequeno" onClick={() => void encerrar()}>
          Sair
        </button>
      </div>
    </header>
  )
}

export function Leiaute({ titulo, children }: { titulo: string; children: ReactNode }) {
  return (
    <div className="aplicacao">
      <Lateral />
      <div className="principal">
        <Cabecalho titulo={titulo} />
        <main className="conteudo" id="conteudo">
          {children}
        </main>
      </div>
    </div>
  )
}
