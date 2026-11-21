import { createContext, useContext } from 'react'
import type { Modulo, Usuario } from '../tipos/api'

export type Sessao = {
  usuario: Usuario | null
  verificando: boolean
  aviso: string
  polo: string
  selecionarPolo: (polo: string) => void
  concluirLogin: (token: string, usuario: Usuario) => void
  encerrar: () => Promise<void>
  podeVer: (modulo: Modulo) => boolean
  podeEditar: (modulo: Modulo) => boolean
}

export const ContextoSessao = createContext<Sessao | null>(null)

export function useSessao(): Sessao {
  const sessao = useContext(ContextoSessao)
  if (!sessao) throw new Error('useSessao precisa estar dentro de <ProvedorSessao>.')
  return sessao
}
