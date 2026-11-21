import { useCallback, useEffect, useState } from 'react'
import { listarOrdens } from '../servicos/ordensServico'
import type { FiltroOrdens } from '../tipos/api'
import { useConsulta } from './useConsulta'

const ATUALIZACAO_MS = 60_000 // HU-008 CA04: a cor do atraso muda em até 1 min sem recarregar.
const FILTRO_INICIAL: FiltroOrdens = { estado: 'PENDENTE', busca: '', atrasada: false, page: 1 }

/** Filtro + lista de OSs do polo do cabeçalho, recarregada a cada minuto.
 * A troca de polo remonta a página (key no App), o que refaz a consulta. */
export function useOrdensServico() {
  const [filtro, setFiltro] = useState<FiltroOrdens>(FILTRO_INICIAL)
  const carregar = useCallback(() => listarOrdens(filtro), [filtro])
  const consulta = useConsulta(carregar)
  const { recarregar } = consulta

  useEffect(() => {
    const id = window.setInterval(recarregar, ATUALIZACAO_MS)
    return () => window.clearInterval(id)
  }, [recarregar])

  const alterarFiltro = useCallback((mudanca: Partial<FiltroOrdens>) => {
    setFiltro((atual) => ({ ...atual, page: 1, ...mudanca }))
  }, [])

  return { filtro, alterarFiltro, consulta }
}
