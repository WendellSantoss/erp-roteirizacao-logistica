import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { ListaVazia } from '../../componentes/ListaVazia'
import type { Consulta } from '../../hooks/useConsulta'
import type { ImportacaoResumo, ListaPaginada } from '../../tipos/api'
import { formatarDataHora } from '../../utilitarios/formatacao'

function Tabela({ importacoes }: { importacoes: ImportacaoResumo[] }) {
  if (importacoes.length === 0) return <ListaVazia titulo="Nenhuma importação ainda neste filtro" />
  return (
    <div className="tabela-rolagem">
      <table className="tabela">
        <caption className="oculto-visualmente">Últimas importações</caption>
        <thead>
          <tr>
            {[
              'Data',
              'Polo',
              'Arquivo',
              'Usuário',
              'Status',
              'Linhas',
              'Novas',
              'Atualizadas',
              'Fora de escopo',
            ].map((c) => (
              <th scope="col" key={c}>
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {importacoes.map((item) => (
            <tr key={item.id}>
              <td className="mono">{formatarDataHora(item.iniciada_em)}</td>
              <td>{item.polo}</td>
              <td>{item.nome_arquivo}</td>
              <td>{item.usuario}</td>
              <td>{item.status}</td>
              <td className="mono">{item.total_linhas}</td>
              <td className="mono">{item.novas}</td>
              <td className="mono">{item.atualizadas}</td>
              <td className="mono">{item.fora_escopo}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function HistoricoImportacoes({
  consulta,
}: {
  consulta: Consulta<ListaPaginada<ImportacaoResumo>>
}) {
  return (
    <section
      aria-labelledby="titulo-historico"
      style={{ display: 'flex', flexDirection: 'column', gap: 10 }}
    >
      <h2 id="titulo-historico">Últimas importações</h2>
      <EstadoDaConsulta consulta={consulta}>
        {(lista) => <Tabela importacoes={lista.resultados} />}
      </EstadoDaConsulta>
    </section>
  )
}
