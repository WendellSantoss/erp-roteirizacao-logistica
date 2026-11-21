import { useEffect, useState } from 'react'

/** Muda a cada `intervaloMs`; serve para recalcular o atraso sem recarregar a página (HU-008 CA04). */
export function useRelogio(intervaloMs: number): number {
  const [instante, setInstante] = useState(() => Date.now())
  useEffect(() => {
    const id = window.setInterval(() => setInstante(Date.now()), intervaloMs)
    return () => window.clearInterval(id)
  }, [intervaloMs])
  return instante
}
