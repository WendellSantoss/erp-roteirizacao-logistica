import { useCallback, useMemo, useState } from 'react'
import type { OrdemNoMapa } from '../tipos/api'
import { pontoNoPoligono, somarSelecao, type Ponto } from '../utilitarios/geometria'

export type SelecaoOrdens = {
  selecionadas: number[]
  estaSelecionada: (id: number) => boolean
  selecionarPorPoligono: (poligono: Ponto[]) => number
  alternar: (id: number) => void
  limpar: () => void
}

/** Seleção do Roteirizador (HU-012, HU-031). Só OSs aptas que estão no mapa entram. */
export function useSelecaoOrdens(ordensAptas: OrdemNoMapa[]): SelecaoOrdens {
  const [ids, setIds] = useState<number[]>([])
  // OS que saiu do mapa (ex.: entrou numa rota) sai da seleção sem precisar de efeito.
  const disponiveis = useMemo(() => new Set(ordensAptas.map((o) => o.id)), [ordensAptas])
  const selecionadas = useMemo(() => ids.filter((id) => disponiveis.has(id)), [ids, disponiveis])
  const conjunto = useMemo(() => new Set(selecionadas), [selecionadas])

  const selecionarPorPoligono = useCallback(
    (poligono: Ponto[]) => {
      const dentro = ordensAptas.filter((o) => pontoNoPoligono(o, poligono)).map((o) => o.id)
      if (dentro.length) setIds((atuais) => somarSelecao(atuais, dentro))
      return dentro.length
    },
    [ordensAptas],
  )
  const alternar = useCallback(
    (id: number) =>
      setIds((atuais) => (atuais.includes(id) ? atuais.filter((x) => x !== id) : [...atuais, id])),
    [],
  )
  const limpar = useCallback(() => setIds([]), [])
  const estaSelecionada = useCallback((id: number) => conjunto.has(id), [conjunto])
  return { selecionadas, estaSelecionada, selecionarPorPoligono, alternar, limpar }
}
