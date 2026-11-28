import { useCallback, useState } from 'react'
import { lerPlanejamento, gravarPlanejamento } from '../servicos/armazenamento'
import { consultarPlanejamento } from '../servicos/roteirizacao'
import type { ChavePlanejamento } from '../tipos/api'
import { dataDeAmanha } from '../utilitarios/formatacao'
import { useConsulta } from './useConsulta'

type Escolha = { operacaoId: number | null; data: string }

function escolhaInicial(): Escolha {
  try {
    const salva = JSON.parse(lerPlanejamento() ?? 'null') as Escolha | null
    if (salva?.data) return salva
  } catch {
    // Valor corrompido no armazenamento: volta ao padrão.
  }
  // HU-011 RN-L02: a data padrão é amanhã.
  return { operacaoId: null, data: dataDeAmanha() }
}

/** Operação e data do Roteirizador, lembradas na sessão (HU-011 CA04). */
export function useEscolhaPlanejamento() {
  const [escolha, setEscolha] = useState<Escolha>(escolhaInicial)
  const alterar = useCallback((parcial: Partial<Escolha>) => {
    setEscolha((atual) => {
      const nova = { ...atual, ...parcial }
      gravarPlanejamento(JSON.stringify(nova))
      return nova
    })
  }, [])
  const chave: ChavePlanejamento | null =
    escolha.operacaoId === null ? null : { operacao_id: escolha.operacaoId, data: escolha.data }
  return { escolha, alterar, chave }
}

export function usePlanejamento(chave: ChavePlanejamento) {
  const { operacao_id: operacaoId, data } = chave
  const carregar = useCallback(
    () => consultarPlanejamento({ operacao_id: operacaoId, data }),
    [operacaoId, data],
  )
  return useConsulta(carregar)
}
