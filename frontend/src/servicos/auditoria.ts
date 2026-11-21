import type { Lista, RegistroAuditoria } from '../tipos/api'
import { requisitar } from './cliente'

export function listarAuditoria(): Promise<Lista<RegistroAuditoria>> {
  return requisitar<Lista<RegistroAuditoria>>('/api/v1/auditoria/')
}
