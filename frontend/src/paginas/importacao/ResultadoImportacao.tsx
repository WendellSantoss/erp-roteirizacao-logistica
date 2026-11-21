import type { Importacao } from '../../tipos/api'

function Numero({ rotulo, valor }: { rotulo: string; valor: number }) {
  return (
    <div className="cartao">
      <div className="texto-suave">{rotulo}</div>
      <div className="numero-resumo">{valor}</div>
    </div>
  )
}

/** Resumo da importação (HU-004 CA01, HU-003 CA01) e log de alertas por linha (HU-002 CA03). */
export function ResultadoImportacao({
  importacao,
  nomePolo,
}: {
  importacao: Importacao
  nomePolo: string
}) {
  const { resumo } = importacao
  const nadaNoEscopo = resumo.novas + resumo.atualizadas === 0 && resumo.fora_escopo > 0
  return (
    <section
      className="cartao"
      aria-labelledby="titulo-resultado"
      style={{ display: 'flex', flexDirection: 'column', gap: 12 }}
    >
      <h2 id="titulo-resultado">Importação de {importacao.nome_arquivo} concluída</h2>
      {nadaNoEscopo && (
        <div className="aviso aviso-alerta">Nenhuma OS do escopo do {nomePolo} nesta planilha.</div>
      )}
      <div className="grade-resumo">
        <Numero rotulo="Linhas lidas" valor={resumo.total_linhas} />
        <Numero rotulo="Novas OSs" valor={resumo.novas} />
        <Numero rotulo="OSs atualizadas (upsert)" valor={resumo.atualizadas} />
        <Numero rotulo="Ignorados (fora de escopo)" valor={resumo.fora_escopo} />
      </div>
      <p className="texto-suave mono" style={{ margin: 0, wordBreak: 'break-all' }}>
        SHA-256: {importacao.hash_sha256}
      </p>
      {importacao.alertas.length > 0 && (
        <div className="tabela-rolagem">
          <table className="tabela">
            <caption className="oculto-visualmente">Alertas da importação</caption>
            <thead>
              <tr>
                <th scope="col">Linha</th>
                <th scope="col">Campo</th>
                <th scope="col">Motivo</th>
              </tr>
            </thead>
            <tbody>
              {importacao.alertas.map((alerta, indice) => (
                <tr key={indice}>
                  <td className="mono">{alerta.linha}</td>
                  <td>{alerta.campo}</td>
                  <td>{alerta.motivo}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
