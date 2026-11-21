// Esqueleto ambulante (Etapa 2): status da API e do banco.
import { requisitar } from './cliente'

export type StatusSaude = {
  status: string
  database: string
}

export function consultarSaude(): Promise<StatusSaude> {
  return requisitar<StatusSaude>('/health')
}
