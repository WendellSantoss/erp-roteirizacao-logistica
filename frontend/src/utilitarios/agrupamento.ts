import type { OrdemNoMapa } from '../tipos/api'

/** OSs da mesma unidade dividem a coordenada; o mapa mostra um pin por local com a contagem. */
export type LocalNoMapa = {
  chave: string
  latitude: number
  longitude: number
  unidade: string
  ordens: OrdemNoMapa[]
}

export function agruparPorLocal(ordens: OrdemNoMapa[]): LocalNoMapa[] {
  const locais = new Map<string, LocalNoMapa>()
  for (const ordem of ordens) {
    const chave = `${ordem.latitude},${ordem.longitude}`
    const local = locais.get(chave)
    if (local) local.ordens.push(ordem)
    else
      locais.set(chave, {
        chave,
        latitude: ordem.latitude,
        longitude: ordem.longitude,
        unidade: ordem.unidade.nome,
        ordens: [ordem],
      })
  }
  return [...locais.values()]
}
