import type {
  ArquivoRpa,
  ChavePlanejamento,
  Lista,
  Operacao,
  PedidoRota,
  Planejamento,
  Rota,
} from '../tipos/api'
import { baixar, requisitar } from './cliente'

const BASE = '/api/v1/roteirizacao'

export function listarOperacoes(): Promise<Lista<Operacao>> {
  return requisitar<Lista<Operacao>>(`${BASE}/operacoes/`)
}

export function consultarPlanejamento(chave: ChavePlanejamento): Promise<Planejamento> {
  return requisitar<Planejamento>(`${BASE}/planejamento/`, { consulta: chave })
}

export function criarRota(pedido: PedidoRota): Promise<Rota> {
  return requisitar<Rota>(`${BASE}/rotas/`, { metodo: 'POST', corpo: pedido })
}

export function finalizarPlanejamento(chave: ChavePlanejamento): Promise<unknown> {
  return requisitar(`${BASE}/planejamento/finalizar/`, { metodo: 'POST', corpo: chave })
}

export function gerarArquivoRpa(chave: ChavePlanejamento): Promise<ArquivoRpa> {
  return requisitar<ArquivoRpa>(`${BASE}/planejamento/arquivo-rpa/`, {
    metodo: 'POST',
    corpo: chave,
  })
}

export function baixarArquivoRpa(chave: ChavePlanejamento): Promise<Blob> {
  return baixar(`${BASE}/planejamento/arquivo-rpa/`, chave)
}
