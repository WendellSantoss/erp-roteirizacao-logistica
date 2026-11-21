import { useSyncExternalStore } from 'react'

// Roteador mínimo sobre a History API: evita uma dependência só para meia dúzia de telas.
const EVENTO_NAVEGACAO = 'genios:navegacao'

function inscrever(aoMudar: () => void) {
  window.addEventListener('popstate', aoMudar)
  window.addEventListener(EVENTO_NAVEGACAO, aoMudar)
  return () => {
    window.removeEventListener('popstate', aoMudar)
    window.removeEventListener(EVENTO_NAVEGACAO, aoMudar)
  }
}

export function navegar(caminho: string, substituir = false) {
  if (caminho === window.location.pathname) return
  if (substituir) window.history.replaceState(null, '', caminho)
  else window.history.pushState(null, '', caminho)
  window.dispatchEvent(new Event(EVENTO_NAVEGACAO))
}

export function useRota(): string {
  return useSyncExternalStore(inscrever, () => window.location.pathname)
}
