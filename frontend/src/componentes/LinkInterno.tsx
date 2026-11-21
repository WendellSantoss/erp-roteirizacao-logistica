import type { MouseEvent, ReactNode } from 'react'
import { navegar, useRota } from '../hooks/useRota'

/** Link da SPA: navega sem recarregar e marca a página atual para leitores de tela. */
export function LinkInterno({ para, children }: { para: string; children: ReactNode }) {
  const rota = useRota()
  const aoClicar = (evento: MouseEvent<HTMLAnchorElement>) => {
    if (evento.metaKey || evento.ctrlKey || evento.shiftKey) return
    evento.preventDefault()
    navegar(para)
  }
  return (
    <a href={para} onClick={aoClicar} aria-current={rota === para ? 'page' : undefined}>
      {children}
    </a>
  )
}
