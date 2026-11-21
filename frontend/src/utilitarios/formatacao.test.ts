import { describe, expect, it } from 'vitest'
import { formatarCoordenada, formatarDataHora, formatarHoras, iniciais } from './formatacao'

describe('formatos da HU-007 (RN-L02)', () => {
  it('CA02: abertura em dd/mm/aaaa hh:mm no fuso da operação', () => {
    expect(formatarDataHora('2026-07-11T08:05:00-03:00')).toBe('11/07/2026 08:05')
  })

  it('CA02: coordenada com 4 casas e vírgula', () => {
    expect(formatarCoordenada(-7.08321)).toBe('-7,0832')
  })

  it('CA03: coordenada ausente vira travessão', () => {
    expect(formatarCoordenada(null)).toBe('—')
  })

  it('HU-008 CA01: decorrido e atraso em "Xh Ymin"', () => {
    expect(formatarHoras(30)).toBe('30h 0min')
    expect(formatarHoras(2.5)).toBe('2h 30min')
    expect(formatarHoras(-3.25)).toBe('3h 15min')
  })

  it('HU-019 CA01: iniciais do nome no cabeçalho', () => {
    expect(iniciais('Ana Duarte')).toBe('AD')
  })
})
