// Tipos que espelham docs/contrato-api.md. Mudou o contrato, muda aqui.

export type Modulo = 'importacao' | 'pendencias' | 'equipes' | 'almoxarifado' | 'auditoria'

export type Polo = { id: number; codigo: string; nome: string }

export type Usuario = {
  id: number
  nome: string
  email: string
  perfil: string
  pode_visualizar_todos: boolean
  polos_autorizados: Polo[]
  modulos: Modulo[]
  modulos_editaveis: Modulo[]
}

export type RespostaLogin = { access_token: string; usuario: Usuario }

export type CorpoErro = {
  erro: { codigo: string; mensagem: string; detalhes: Record<string, unknown> }
}

export type EstadoOS =
  | 'PENDENTE'
  | 'APTA_A_ROTEIRIZAR'
  | 'DESCONSIDERADA'
  | 'ROTEIRIZADA'
  | 'DESPACHADA'
  | 'EXECUTADA'
  | 'INVALIDADA'
  | 'VALIDADA'
  | 'FATURADA'

export type OrdemServico = {
  id: number
  numero: string
  polo: { id: number; nome: string }
  unidade: { codigo: string; nome: string; latitude: number | null; longitude: number | null }
  tipo: string
  especificacao: string
  numero_imovel: string
  cidade: string
  setor: string
  quadra: string
  estado: EstadoOS
  prioridade: boolean
  desconsiderada: boolean
  equipe_id: number | null
  abertura: string
  prazo_horas: number
  tempo_decorrido_horas: number
  atraso_horas: number
  em_atraso: boolean
}

export type PaginaOrdens = {
  total: number
  contadores_por_status: Partial<Record<EstadoOS, number>>
  resultados: OrdemServico[]
}

export type FiltroOrdens = {
  estado: EstadoOS
  busca: string
  atrasada: boolean
  page: number
}

export type AlertaImportacao = { linha: number; campo: string; motivo: string }

export type StatusImportacao =
  'RECEBIDA' | 'VALIDANDO' | 'FILTRANDO' | 'GRAVANDO' | 'CONCLUIDA' | 'RECUSADA' | 'FALHOU'

export type Importacao = {
  id: number
  polo_id: number
  nome_arquivo: string
  status: StatusImportacao
  hash_sha256: string
  resumo: { total_linhas: number; novas: number; atualizadas: number; fora_escopo: number }
  alertas: AlertaImportacao[]
  motivo_falha: string | null
  iniciada_em: string
  concluida_em: string | null
}

export type ImportacaoResumo = {
  id: number
  polo: string
  usuario: string
  nome_arquivo: string
  status: StatusImportacao
  total_linhas: number
  novas: number
  atualizadas: number
  fora_escopo: number
  iniciada_em: string
}

export type Equipe = { id: number; codigo: string; nome: string; polo_id: number; ativa: boolean }

export type LimiteKit = {
  kit_id: number
  tipo_kit: string
  nome: string
  executado_dia_anterior: number
  saidas_registradas_hoje: number
  saldo_disponivel_hoje: number
}

export type LimitesDoDia = { polo_id: number; data_referencia: string; kits: LimiteKit[] }

export type SaidaKit = {
  id: number
  polo: string
  equipe: string
  tipo_kit: string
  quantidade: number
  data_saida: string
  registrado_por: string
}

export type PedidoSaidaKit = { equipe_id: number; kit_id: number; quantidade: number }

export type RegistroAuditoria = {
  id: number
  entidade: string
  entidade_id: number | null
  campo: string
  valor_anterior: unknown
  valor_novo: unknown
  justificativa: string
  autor: string
  origem: string
  registrado_em: string
}

export type Lista<T> = { resultados: T[] }
export type ListaPaginada<T> = { total: number; resultados: T[] }
