import { ListaVazia } from '../../componentes/ListaVazia'
import type { SaidaKit } from '../../tipos/api'
import { formatarDataHora } from '../../utilitarios/formatacao'

export function TabelaSaidas({ saidas }: { saidas: SaidaKit[] }) {
  if (saidas.length === 0) return <ListaVazia titulo="Nenhuma saída registrada hoje" />
  return (
    <div className="tabela-rolagem">
      <table className="tabela">
        <caption className="oculto-visualmente">Saídas de kits registradas hoje</caption>
        <thead>
          <tr>
            {['Horário', 'Polo', 'Equipe', 'Kit', 'Quantidade', 'Registrado por'].map((coluna) => (
              <th scope="col" key={coluna}>
                {coluna}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {saidas.map((saida) => (
            <tr key={saida.id}>
              <td className="mono">{formatarDataHora(saida.data_saida)}</td>
              <td>{saida.polo}</td>
              <td>{saida.equipe}</td>
              <td>{saida.tipo_kit}</td>
              <td className="mono">{saida.quantidade}</td>
              <td>{saida.registrado_por}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
