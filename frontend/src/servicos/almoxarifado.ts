import type { Equipe, LimitesDoDia, Lista, PedidoSaidaKit, SaidaKit } from '../tipos/api'
import { requisitar } from './cliente'

export function consultarLimites(): Promise<LimitesDoDia> {
  return requisitar<LimitesDoDia>('/api/v1/almoxarifado/limites-kits/')
}

export function listarEquipesAtivas(): Promise<Lista<Equipe>> {
  return requisitar<Lista<Equipe>>('/api/v1/equipes/', { consulta: { ativa: true } })
}

export function listarSaidasDoDia(data: string): Promise<Lista<SaidaKit>> {
  return requisitar<Lista<SaidaKit>>('/api/v1/almoxarifado/saidas-kits/', { consulta: { data } })
}

export function registrarSaida(pedido: PedidoSaidaKit): Promise<unknown> {
  return requisitar('/api/v1/almoxarifado/saidas-kits/', { metodo: 'POST', corpo: pedido })
}
