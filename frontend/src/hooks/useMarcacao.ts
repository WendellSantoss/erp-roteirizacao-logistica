import { useState } from 'react'

/** Conjunto de ids marcados numa lista (HU-060: liberar em lote). */
export function useMarcacao() {
  const [marcadas, setMarcadas] = useState<number[]>([])
  const aoAlternar = (id: number) =>
    setMarcadas((atuais) =>
      atuais.includes(id) ? atuais.filter((x) => x !== id) : [...atuais, id],
    )
  return {
    marcadas,
    estaMarcada: (id: number) => marcadas.includes(id),
    aoAlternar,
    limpar: () => setMarcadas([]),
  }
}
