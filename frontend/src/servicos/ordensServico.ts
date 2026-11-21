import type { FiltroOrdens, PaginaOrdens } from '../tipos/api'
import { requisitar } from './cliente'

export const TAMANHO_PAGINA = 50

export function listarOrdens(filtro: FiltroOrdens): Promise<PaginaOrdens> {
  return requisitar<PaginaOrdens>('/api/v1/ordens-servico/', {
    consulta: {
      estado: filtro.estado,
      busca: filtro.busca.trim(),
      atrasada: filtro.atrasada ? true : undefined,
      page: filtro.page,
      page_size: TAMANHO_PAGINA,
    },
  })
}

type ResumoAlteracao = { id: number; numero: string; prioridade: boolean; estado: string }

export function marcarPrioridade(ordemId: number, prioridade: boolean): Promise<ResumoAlteracao> {
  return requisitar<ResumoAlteracao>(`/api/v1/ordens-servico/${ordemId}/prioridade/`, {
    metodo: 'PATCH',
    corpo: { prioridade },
  })
}

export function desconsiderarOrdem(
  ordemId: number,
  justificativa: string,
): Promise<ResumoAlteracao> {
  return requisitar<ResumoAlteracao>(`/api/v1/ordens-servico/${ordemId}/desconsiderar/`, {
    metodo: 'POST',
    corpo: { justificativa },
  })
}
