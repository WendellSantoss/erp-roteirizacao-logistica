// Formatos da HU-007 RN-L02 (datas dd/mm/aaaa hh:mm, horas "Xh Ymin", coordenadas com vírgula).

const FUSO_OPERACAO = 'America/Fortaleza' // HU-008 RN-L04

const formatoDataHora = new Intl.DateTimeFormat('pt-BR', {
  timeZone: FUSO_OPERACAO,
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
})

export function formatarDataHora(iso: string | null): string {
  if (!iso) return '—'
  return formatoDataHora.format(new Date(iso)).replace(',', '')
}

export function formatarHoras(horas: number): string {
  const minutosTotais = Math.round(Math.abs(horas) * 60)
  return `${Math.floor(minutosTotais / 60)}h ${minutosTotais % 60}min`
}

export function formatarCoordenada(valor: number | null): string {
  if (valor === null || valor === undefined) return '—'
  return Number(valor).toFixed(4).replace('.', ',')
}

export function dataDeHoje(): string {
  return new Intl.DateTimeFormat('en-CA', { timeZone: FUSO_OPERACAO }).format(new Date())
}

export const ROTULOS_PERFIL: Record<string, string> = {
  GERENTE_CONTRATO: 'Gerente de Contrato',
  COORDENADOR: 'Coordenador',
  ANALISTA_OPERACOES: 'Analista de Operações',
  ALMOXARIFE: 'Almoxarife',
  AUDITOR: 'Auditor',
  ADMINISTRADOR: 'Administrador',
}

export const ROTULOS_ESTADO: Record<string, string> = {
  PENDENTE: 'Pendente',
  APTA_A_ROTEIRIZAR: 'Apta a roteirizar',
  DESCONSIDERADA: 'Desconsiderada',
  ROTEIRIZADA: 'Roteirizada',
  DESPACHADA: 'Despachada',
  EXECUTADA: 'Executada',
  INVALIDADA: 'Invalidada',
  VALIDADA: 'Validada',
  FATURADA: 'Faturada',
}

export function iniciais(nome: string): string {
  const partes = nome.trim().split(/\s+/)
  return (partes[0][0] + (partes.length > 1 ? partes[partes.length - 1][0] : '')).toUpperCase()
}

export function dataDeAmanha(): string {
  const amanha = new Date(Date.now() + 24 * 60 * 60 * 1000)
  return new Intl.DateTimeFormat('en-CA', { timeZone: FUSO_OPERACAO }).format(amanha)
}

/** "2026-07-12" → "12/07/2026", sem passar por Date (evita deslocar o dia pelo fuso). */
export function formatarData(iso: string): string {
  const [ano, mes, dia] = iso.split('-')
  return `${dia}/${mes}/${ano}`
}
