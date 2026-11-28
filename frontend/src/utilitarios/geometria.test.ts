import { describe, expect, it } from 'vitest'
import { pontoNoPoligono, somarSelecao, type Ponto } from './geometria'

const quadrado: Ponto[] = [
  { latitude: 0, longitude: 0 },
  { latitude: 0, longitude: 10 },
  { latitude: 10, longitude: 10 },
  { latitude: 10, longitude: 0 },
]

describe('pontoNoPoligono (HU-012)', () => {
  it('CA01: ponto dentro é selecionado', () => {
    expect(pontoNoPoligono({ latitude: 5, longitude: 5 }, quadrado)).toBe(true)
  })

  it('CA02: ponto fora não é selecionado', () => {
    expect(pontoNoPoligono({ latitude: 11, longitude: 5 }, quadrado)).toBe(false)
    expect(pontoNoPoligono({ latitude: 5, longitude: -0.1 }, quadrado)).toBe(false)
  })

  it('RN-L01: ponto sobre a borda ou num vértice conta como dentro', () => {
    expect(pontoNoPoligono({ latitude: 0, longitude: 5 }, quadrado)).toBe(true)
    expect(pontoNoPoligono({ latitude: 10, longitude: 10 }, quadrado)).toBe(true)
  })

  it('polígono côncavo exclui a reentrância', () => {
    const emU: Ponto[] = [
      { latitude: 0, longitude: 0 },
      { latitude: 0, longitude: 9 },
      { latitude: 9, longitude: 9 },
      { latitude: 9, longitude: 6 },
      { latitude: 3, longitude: 6 },
      { latitude: 3, longitude: 3 },
      { latitude: 9, longitude: 3 },
      { latitude: 9, longitude: 0 },
    ]
    expect(pontoNoPoligono({ latitude: 6, longitude: 4.5 }, emU)).toBe(false)
    expect(pontoNoPoligono({ latitude: 6, longitude: 1 }, emU)).toBe(true)
  })

  it('menos de três vértices não seleciona nada', () => {
    expect(pontoNoPoligono({ latitude: 0, longitude: 0 }, quadrado.slice(0, 2))).toBe(false)
  })

  it('CA07: 2.000 pontos são avaliados bem abaixo de 1 s', () => {
    const pontos = Array.from({ length: 2000 }, (_, i) => ({
      latitude: (i % 50) / 4,
      longitude: Math.floor(i / 50) / 4,
    }))
    const inicio = performance.now()
    const dentro = pontos.filter((p) => pontoNoPoligono(p, quadrado))
    expect(performance.now() - inicio).toBeLessThan(1000)
    expect(dentro.length).toBeGreaterThan(0)
  })
})

describe('somarSelecao (HU-012 CA04)', () => {
  it('segundo polígono soma sem duplicar', () => {
    const primeiro = Array.from({ length: 42 }, (_, i) => i)
    const segundo = [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
    expect(somarSelecao(primeiro, segundo)).toHaveLength(49)
  })
})
