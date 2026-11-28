// Tipos que espelham docs/contrato-api.md. Mudou o contrato, muda aqui.

export type Modulo =
  | 'importacao'
  | 'webscraper'
  | 'pendencias'
  | 'roteirizador'
  | 'equipes'
  | 'almoxarifado'
  | 'auditoria'

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

export type Equipe = {
  id: number
  codigo: string
  nome: string
  polo_id: number
  ativa: boolean
  placa: string
  capacidade_diaria: number
}

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

// ── Coordenadas (HU-024) e liberação (HU-060) ─────────────────────────────

export type Unidade = {
  id: number
  codigo: string
  nome: string
  polo_id: number
  polo: string
  latitude: string | null
  longitude: string | null
  coordenada_manual: boolean
  total_ordens: number
}

export type ResultadoLiberacao = {
  liberadas: string[]
  nao_liberadas: { numero: string; motivo: string }[]
}

// ── Roteirizador (HU-011, HU-012, HU-056, HU-013, HU-014) ────────────────

export type Operacao = { id: number; codigo: string; nome: string }

export type OrdemNoMapa = {
  id: number
  numero: string
  tipo: string
  especificacao: string
  prioridade: boolean
  unidade: { codigo: string; nome: string }
  latitude: number
  longitude: number
}

export type Rota = {
  id: number
  nome: string
  cor: string
  observacao: string
  previsao_inicio: string
  carregamento: string
  equipe: { id: number; codigo: string; nome: string; placa: string; ativa: boolean }
  ordens: OrdemNoMapa[]
}

export type StatusPlanejamento = 'ABERTO' | 'FINALIZADO' | 'DESPACHADO'

export type ArquivoRpa = {
  nome_arquivo: string
  hash_sha256: string
  total_ordens: number
  gerado_por: string | null
  gerado_em: string
}

export type Planejamento = {
  operacao: Operacao
  data: string
  planejamento: {
    id: number | null
    status: StatusPlanejamento
    somente_leitura: boolean
    motivo_somente_leitura: string
    finalizado_em: string | null
    finalizado_por: string | null
    arquivo_rpa: ArquivoRpa | null
  }
  rotas: Rota[]
  ordens_aptas: OrdemNoMapa[]
}

export type ChavePlanejamento = { operacao_id: number; data: string }

export type PedidoRota = ChavePlanejamento & {
  nome: string
  equipe_id: number
  previsao_inicio: string
  carregamento: string
  cor: string
  observacao: string
  ordens_ids: number[]
}
