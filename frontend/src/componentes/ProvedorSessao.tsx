import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'
import { ContextoSessao, type Sessao } from '../hooks/contextoSessao'
import { gravarPolo, gravarToken, lerPolo, lerToken } from '../servicos/armazenamento'
import { consultarUsuarioAtual, sair } from '../servicos/autenticacao'
import { definirPoloDasRequisicoes, EVENTO_SESSAO_EXPIRADA, POLO_TODOS } from '../servicos/cliente'
import type { Modulo, Usuario } from '../tipos/api'

/** Polo salvo se ainda for permitido; com um único polo, ele; senão "Todos". */
function poloInicial(usuario: Usuario): string {
  const salvo = lerPolo()
  const permitidos = usuario.polos_autorizados.map((polo) => String(polo.id))
  if (salvo && (salvo === POLO_TODOS || permitidos.includes(salvo))) return salvo
  return permitidos.length === 1 ? permitidos[0] : POLO_TODOS
}

export function ProvedorSessao({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null)
  const [verificando, setVerificando] = useState(() => Boolean(lerToken()))
  const [aviso, setAviso] = useState('')
  const [polo, setPolo] = useState(POLO_TODOS)

  const selecionarPolo = useCallback((novo: string) => {
    definirPoloDasRequisicoes(novo)
    gravarPolo(novo)
    setPolo(novo)
  }, [])

  const aplicarUsuario = useCallback(
    (novoUsuario: Usuario) => {
      selecionarPolo(poloInicial(novoUsuario))
      setUsuario(novoUsuario)
    },
    [selecionarPolo],
  )

  useEffect(() => {
    if (!lerToken()) return
    consultarUsuarioAtual()
      .then(aplicarUsuario)
      .catch(() => gravarToken(null))
      .finally(() => setVerificando(false))
  }, [aplicarUsuario])

  useEffect(() => {
    const expirar = () => {
      gravarToken(null)
      setUsuario(null)
      setAviso('Sessão expirada. Entre novamente.')
    }
    window.addEventListener(EVENTO_SESSAO_EXPIRADA, expirar)
    return () => window.removeEventListener(EVENTO_SESSAO_EXPIRADA, expirar)
  }, [])

  const sessao = useMemo<Sessao>(
    () => ({
      usuario,
      verificando,
      aviso,
      polo,
      selecionarPolo,
      concluirLogin: (token, novoUsuario) => {
        gravarToken(token)
        setAviso('')
        aplicarUsuario(novoUsuario)
      },
      encerrar: async () => {
        await sair().catch(() => undefined)
        gravarToken(null)
        setUsuario(null)
      },
      podeVer: (modulo: Modulo) => Boolean(usuario?.modulos.includes(modulo)),
      podeEditar: (modulo: Modulo) => Boolean(usuario?.modulos_editaveis.includes(modulo)),
    }),
    [usuario, verificando, aviso, polo, selecionarPolo, aplicarUsuario],
  )

  return <ContextoSessao.Provider value={sessao}>{children}</ContextoSessao.Provider>
}
