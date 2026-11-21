import type { Importacao, ImportacaoResumo, ListaPaginada } from '../tipos/api'
import { requisitar } from './cliente'

export function enviarPlanilha(arquivo: File): Promise<Importacao> {
  const formulario = new FormData()
  formulario.append('arquivo', arquivo)
  return requisitar<Importacao>('/api/v1/importacoes/', { metodo: 'POST', formulario })
}

export function listarImportacoes(): Promise<ListaPaginada<ImportacaoResumo>> {
  return requisitar<ListaPaginada<ImportacaoResumo>>('/api/v1/importacoes/', {
    consulta: { page_size: 10 },
  })
}
