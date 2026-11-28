// Cliente HTTP único da aplicação (AGENTS.md §2): só a pasta servicos/ chama fetch.
import type { CorpoErro } from '../tipos/api'
import { lerToken } from './armazenamento'

const URL_API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

export const POLO_TODOS = 'TODOS'
export const EVENTO_SESSAO_EXPIRADA = 'genios:sessao-expirada'

let poloAtual = POLO_TODOS

/** Polo enviado no cabeçalho X-Polo-Id de todas as requisições (contrato §1). */
export function definirPoloDasRequisicoes(polo: string) {
  poloAtual = polo
}

export class ErroApi extends Error {
  status: number
  codigo: string
  detalhes: Record<string, unknown>

  constructor(status: number, corpo: CorpoErro['erro']) {
    super(corpo.mensagem)
    this.status = status
    this.codigo = corpo.codigo
    this.detalhes = corpo.detalhes
  }
}

const ERRO_DE_REDE = {
  codigo: 'SEM_CONEXAO',
  mensagem:
    'Não foi possível falar com a API. Se o servidor estava hibernando, aguarde cerca de 1 minuto e tente de novo.',
  detalhes: {},
}

type Consulta = Record<string, string | number | boolean | undefined>
type Opcoes = { metodo?: string; corpo?: unknown; formulario?: FormData; consulta?: Consulta }

function montarUrl(caminho: string, consulta: Consulta = {}) {
  const parametros = new URLSearchParams()
  Object.entries(consulta).forEach(([chave, valor]) => {
    if (valor !== undefined && valor !== '') parametros.set(chave, String(valor))
  })
  const texto = parametros.toString()
  return `${URL_API}${caminho}${texto ? `?${texto}` : ''}`
}

function montarCabecalhos(opcoes: Opcoes): Headers {
  const cabecalhos = new Headers({ Accept: 'application/json', 'X-Polo-Id': poloAtual })
  const token = lerToken()
  if (token) cabecalhos.set('Authorization', `Bearer ${token}`)
  if (opcoes.corpo !== undefined) cabecalhos.set('Content-Type', 'application/json')
  return cabecalhos
}

async function lerErro(resposta: Response): Promise<ErroApi> {
  try {
    const corpo = (await resposta.json()) as CorpoErro
    return new ErroApi(resposta.status, corpo.erro)
  } catch {
    const mensagem = `A API respondeu com erro ${resposta.status}.`
    return new ErroApi(resposta.status, { codigo: 'ERRO', mensagem, detalhes: {} })
  }
}

function corpoDaRequisicao(opcoes: Opcoes): BodyInit | undefined {
  if (opcoes.formulario) return opcoes.formulario
  return opcoes.corpo === undefined ? undefined : JSON.stringify(opcoes.corpo)
}

async function enviar(caminho: string, opcoes: Opcoes): Promise<Response> {
  try {
    return await fetch(montarUrl(caminho, opcoes.consulta), {
      method: opcoes.metodo ?? 'GET',
      headers: montarCabecalhos(opcoes),
      body: corpoDaRequisicao(opcoes),
    })
  } catch {
    throw new ErroApi(0, ERRO_DE_REDE)
  }
}

/** Faz a requisição e devolve o JSON tipado; erro vira ErroApi com a mensagem do contrato. */
export async function requisitar<T>(caminho: string, opcoes: Opcoes = {}): Promise<T> {
  const resposta = await enviar(caminho, opcoes)
  if (resposta.status === 401 && lerToken()) window.dispatchEvent(new Event(EVENTO_SESSAO_EXPIRADA))
  if (!resposta.ok) throw await lerErro(resposta)
  if (resposta.status === 204) return undefined as T
  return (await resposta.json()) as T
}

/** Baixa um arquivo da API (ex.: RPA) e devolve o conteúdo como Blob. */
export async function baixar(caminho: string, consulta: Consulta = {}): Promise<Blob> {
  const resposta = await enviar(caminho, { consulta })
  if (!resposta.ok) throw await lerErro(resposta)
  return resposta.blob()
}

export function mensagemDeErro(erro: unknown): string {
  if (erro instanceof ErroApi) return erro.message
  return 'Ocorreu um erro inesperado. Tente novamente.'
}
