import type { Lista, Unidade } from '../tipos/api'
import { requisitar } from './cliente'

export function listarUnidades(somenteSemCoordenada: boolean): Promise<Lista<Unidade>> {
  return requisitar<Lista<Unidade>>('/api/v1/unidades/', {
    consulta: { sem_coordenada: somenteSemCoordenada ? true : undefined },
  })
}

/** HU-024: o texto vai como digitado; o servidor aceita vírgula ou ponto (CA04). */
export function informarCoordenada(
  unidadeId: number,
  latitude: string,
  longitude: string,
): Promise<Unidade> {
  return requisitar<Unidade>(`/api/v1/unidades/${unidadeId}/coordenada/`, {
    metodo: 'PATCH',
    corpo: { latitude, longitude },
  })
}
