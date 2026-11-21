import type { RespostaLogin, Usuario } from '../tipos/api'
import { requisitar } from './cliente'

export function entrar(email: string, senha: string): Promise<RespostaLogin> {
  return requisitar<RespostaLogin>('/api/v1/auth/login/', {
    metodo: 'POST',
    corpo: { email, senha },
  })
}

export function consultarUsuarioAtual(): Promise<Usuario> {
  return requisitar<Usuario>('/api/v1/auth/me/')
}

export function sair(): Promise<void> {
  return requisitar<void>('/api/v1/auth/logout/', { metodo: 'POST' })
}
