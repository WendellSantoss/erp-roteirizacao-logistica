// Seleção por polígono no navegador (HU-012). O servidor revalida cada OS ao criar a rota.

export type Ponto = { latitude: number; longitude: number }

const TOLERANCIA = 1e-9

function produtoVetorial(a: Ponto, b: Ponto, p: Ponto): number {
  return (
    (b.longitude - a.longitude) * (p.latitude - a.latitude) -
    (b.latitude - a.latitude) * (p.longitude - a.longitude)
  )
}

function estaNoSegmento(a: Ponto, b: Ponto, p: Ponto): boolean {
  if (Math.abs(produtoVetorial(a, b, p)) > TOLERANCIA) return false
  const dentroLatitude =
    p.latitude >= Math.min(a.latitude, b.latitude) - TOLERANCIA &&
    p.latitude <= Math.max(a.latitude, b.latitude) + TOLERANCIA
  const dentroLongitude =
    p.longitude >= Math.min(a.longitude, b.longitude) - TOLERANCIA &&
    p.longitude <= Math.max(a.longitude, b.longitude) + TOLERANCIA
  return dentroLatitude && dentroLongitude
}

function cruzaRaio(a: Ponto, b: Ponto, p: Ponto): boolean {
  if (a.latitude > p.latitude === b.latitude > p.latitude) return false
  const longitudeNoCruzamento =
    a.longitude +
    ((p.latitude - a.latitude) * (b.longitude - a.longitude)) / (b.latitude - a.latitude)
  return p.longitude < longitudeNoCruzamento
}

/** Ray casting; ponto exatamente sobre a borda conta como dentro (HU-012 RN-L01). */
export function pontoNoPoligono(ponto: Ponto, poligono: Ponto[]): boolean {
  if (poligono.length < 3) return false
  let dentro = false
  for (let i = 0, j = poligono.length - 1; i < poligono.length; j = i++) {
    const [a, b] = [poligono[i], poligono[j]]
    if (estaNoSegmento(a, b, ponto)) return true
    if (cruzaRaio(a, b, ponto)) dentro = !dentro
  }
  return dentro
}

/** RN-L02: um novo polígono soma à seleção atual, sem duplicar. */
export function somarSelecao(atual: number[], novos: number[]): number[] {
  return [...new Set([...atual, ...novos])]
}
