import { useCallback, useEffect, useMemo, useState } from 'react'
import { mensagemDeErro } from '../servicos/cliente'

export type Consulta<T> = {
  dados: T | null
  carregando: boolean
  erro: string
  recarregar: () => void
}

type Pedido<T> = { carregar: () => Promise<T>; versao: number }
type Resultado<T> = { pedido: Pedido<T> | null; dados: T | null; erro: string }

/** Executa `carregar` e expõe os três estados exigidos pelo guia: carregando, erro e dados. */
export function useConsulta<T>(carregar: () => Promise<T>): Consulta<T> {
  const [versao, setVersao] = useState(0)
  const pedido = useMemo<Pedido<T>>(() => ({ carregar, versao }), [carregar, versao])
  const [resultado, setResultado] = useState<Resultado<T>>({ pedido: null, dados: null, erro: '' })

  useEffect(() => {
    let ativo = true
    pedido
      .carregar()
      .then((dados) => ativo && setResultado({ pedido, dados, erro: '' }))
      .catch((falha: unknown) => {
        if (ativo)
          setResultado((anterior) => ({ ...anterior, pedido, erro: mensagemDeErro(falha) }))
      })
    return () => {
      ativo = false
    }
  }, [pedido])

  const recarregar = useCallback(() => setVersao((atual) => atual + 1), [])
  // Carregando = o último resultado não corresponde ao pedido atual (sem setState dentro do efeito).
  const carregando = resultado.pedido !== pedido
  return { dados: resultado.dados, carregando, erro: carregando ? '' : resultado.erro, recarregar }
}
