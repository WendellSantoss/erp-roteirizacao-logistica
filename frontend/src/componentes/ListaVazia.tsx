import type { ReactNode } from 'react'

export function ListaVazia({ titulo, children }: { titulo: string; children?: ReactNode }) {
  return (
    <div className="estado-vazio">
      <p style={{ fontWeight: 700, margin: '0 0 4px' }}>{titulo}</p>
      {children && <p style={{ margin: 0 }}>{children}</p>}
    </div>
  )
}
