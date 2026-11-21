export function TituloPagina({ titulo, subtitulo }: { titulo: string; subtitulo: string }) {
  return (
    <div className="titulo-pagina">
      <h1>{titulo}</h1>
      <p className="texto-suave">{subtitulo}</p>
    </div>
  )
}
