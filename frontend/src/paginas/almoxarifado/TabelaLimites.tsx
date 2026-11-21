import type { LimiteKit } from '../../tipos/api'

/** Teto do dia por kit: executado em D−1 menos o que já saiu hoje (RN-11). */
export function TabelaLimites({ kits }: { kits: LimiteKit[] }) {
  return (
    <div className="tabela-rolagem">
      <table className="tabela">
        <caption className="oculto-visualmente">Limites de saída de kits no dia</caption>
        <thead>
          <tr>
            <th scope="col">Kit</th>
            <th scope="col">Executado ontem</th>
            <th scope="col">Saídas hoje</th>
            <th scope="col">Saldo disponível</th>
          </tr>
        </thead>
        <tbody>
          {kits.map((kit) => (
            <tr key={kit.kit_id}>
              <th scope="row">{kit.nome}</th>
              <td className="mono">{kit.executado_dia_anterior} un.</td>
              <td className="mono">{kit.saidas_registradas_hoje} un.</td>
              <td>
                <span
                  className={`selo ${kit.saldo_disponivel_hoje > 0 ? 'selo-ok' : 'selo-atraso'}`}
                >
                  {kit.saldo_disponivel_hoje} un.
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
