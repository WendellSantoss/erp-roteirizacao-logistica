import { describe, expect, it } from 'vitest'
import type { OrdemNoMapa } from '../tipos/api'
import { agruparPorLocal } from './agrupamento'

function ordem(id: number, latitude: number, longitude: number): OrdemNoMapa {
  return {
    id,
    numero: String(id),
    tipo: 'RELIGACAO_AGUA',
    especificacao: 'Religação',
    prioridade: false,
    unidade: { codigo: 'UN', nome: `Unidade ${latitude}` },
    latitude,
    longitude,
  }
}

describe('agruparPorLocal', () => {
  it('junta as OSs da mesma coordenada num único pin', () => {
    const locais = agruparPorLocal([
      ordem(1, -7.1, -34.8),
      ordem(2, -7.1, -34.8),
      ordem(3, -7.2, -34.8),
    ])
    expect(locais).toHaveLength(2)
    expect(locais[0].ordens.map((o) => o.id)).toEqual([1, 2])
  })
})
