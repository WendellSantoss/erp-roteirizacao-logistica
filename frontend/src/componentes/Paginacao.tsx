type Propriedades = {
  pagina: number
  total: number
  tamanho: number
  aoMudar: (pagina: number) => void
}

export function Paginacao({ pagina, total, tamanho, aoMudar }: Propriedades) {
  const ultima = Math.max(1, Math.ceil(total / tamanho))
  return (
    <nav className="paginacao" aria-label="Paginação">
      <span className="texto-suave">
        Página {pagina} de {ultima}
      </span>
      <span style={{ display: 'flex', gap: 8 }}>
        <button
          type="button"
          className="botao botao-pequeno"
          disabled={pagina <= 1}
          onClick={() => aoMudar(pagina - 1)}
        >
          Anterior
        </button>
        <button
          type="button"
          className="botao botao-pequeno"
          disabled={pagina >= ultima}
          onClick={() => aoMudar(pagina + 1)}
        >
          Próxima
        </button>
      </span>
    </nav>
  )
}
