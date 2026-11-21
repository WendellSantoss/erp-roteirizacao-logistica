import { useSessao } from '../hooks/contextoSessao'
import { POLO_TODOS } from '../servicos/cliente'

/** Filtro global de polo do cabeçalho (HU-020, contrato §1: cabeçalho X-Polo-Id). */
export function SeletorPolo() {
  const { usuario, polo, selecionarPolo } = useSessao()
  if (!usuario) return null
  return (
    <label className="campo-linha">
      Polo
      <select
        className="mono"
        value={polo}
        onChange={(evento) => selecionarPolo(evento.target.value)}
        style={{
          font: 'inherit',
          padding: '6px 8px',
          borderRadius: 8,
          border: '1px solid var(--cor-borda)',
        }}
      >
        <option value={POLO_TODOS}>Todos</option>
        {usuario.polos_autorizados.map((item) => (
          <option key={item.id} value={String(item.id)}>
            {item.nome}
          </option>
        ))}
      </select>
    </label>
  )
}
