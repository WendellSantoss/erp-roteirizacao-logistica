import { describe, expect, it } from 'vitest'
import { motivoDeRecusa } from './planilha'

const MB = 1024 * 1024

function arquivo(nome: string, tamanho: number): File {
  const falso = new File(['x'], nome)
  Object.defineProperty(falso, 'size', { value: tamanho })
  return falso
}

describe('validação do envio na tela (HU-001)', () => {
  it('CA01: aceita um .xlsx dentro do limite', () => {
    expect(motivoDeRecusa([arquivo('gsan_os_2026-07-11.xlsx', 4 * MB)])).toBe('')
  })

  it('CA03: recusa .csv e .xls', () => {
    const mensagem = 'Formato não aceito: envie a planilha do GSAN em .xlsx'
    expect(motivoDeRecusa([arquivo('gsan.csv', 1)])).toBe(mensagem)
    expect(motivoDeRecusa([arquivo('gsan.xls', 1)])).toBe(mensagem)
  })

  it('CA04: recusa arquivo acima de 25 MB', () => {
    expect(motivoDeRecusa([arquivo('gsan.xlsx', 26 * MB)])).toBe(
      'Arquivo com 26 MB excede o limite de 25 MB',
    )
  })

  it('CA08: recusa mais de um arquivo', () => {
    expect(motivoDeRecusa([arquivo('a.xlsx', 1), arquivo('b.xlsx', 1)])).toBe(
      'Envie um arquivo por vez',
    )
  })
})
