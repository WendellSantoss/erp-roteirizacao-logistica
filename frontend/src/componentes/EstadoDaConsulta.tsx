import type { ReactNode } from 'react'
import type { Consulta } from '../hooks/useConsulta'
import { Carregando } from './Carregando'
import { MensagemErro } from './MensagemErro'

type Propriedades<T> = { consulta: Consulta<T>; children: (dados: T) => ReactNode }

/** Mostra carregando ou erro; só renderiza o conteúdo quando há dados (AGENTS.md §2). */
export function EstadoDaConsulta<T>({ consulta, children }: Propriedades<T>) {
  if (consulta.erro)
    return <MensagemErro mensagem={consulta.erro} aoTentarDeNovo={consulta.recarregar} />
  if (consulta.dados === null) return <Carregando />
  return <>{children(consulta.dados)}</>
}
