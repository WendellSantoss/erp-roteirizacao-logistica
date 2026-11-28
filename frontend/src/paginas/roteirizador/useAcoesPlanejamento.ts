import { useState } from 'react'
import { ErroApi, mensagemDeErro } from '../../servicos/cliente'
import {
  baixarArquivoRpa,
  finalizarPlanejamento,
  gerarArquivoRpa,
} from '../../servicos/roteirizacao'
import type { ChavePlanejamento } from '../../tipos/api'
import { salvarArquivo } from '../../utilitarios/download'

type Inconsistencia = { rota: string; motivo: string }

function inconsistenciasDo(falha: unknown): Inconsistencia[] {
  if (!(falha instanceof ErroApi)) return []
  const lista = falha.detalhes.inconsistencias
  return Array.isArray(lista) ? (lista as Inconsistencia[]) : []
}

/** Finalizar (HU-013) e gerar/baixar o RPA (HU-014), com mensagem de sucesso ou erro. */
export function useAcoesPlanejamento(chave: ChavePlanejamento, aoConcluir: () => void) {
  const [ocupado, setOcupado] = useState(false)
  const [sucesso, setSucesso] = useState('')
  const [erro, setErro] = useState('')
  const [inconsistencias, setInconsistencias] = useState<Inconsistencia[]>([])

  const executar = async (acao: () => Promise<string>) => {
    setOcupado(true)
    setSucesso('')
    setErro('')
    setInconsistencias([])
    try {
      setSucesso(await acao())
      aoConcluir()
    } catch (falha) {
      setErro(mensagemDeErro(falha))
      setInconsistencias(inconsistenciasDo(falha))
    } finally {
      setOcupado(false)
    }
  }

  const finalizar = () =>
    executar(async () => {
      await finalizarPlanejamento(chave)
      return 'Planejamento finalizado. O arquivo RPA já pode ser gerado.'
    })
  const gerarRpa = () =>
    executar(async () => {
      const arquivo = await gerarArquivoRpa(chave)
      salvarArquivo(await baixarArquivoRpa(chave), arquivo.nome_arquivo)
      return `Arquivo RPA gerado com ${arquivo.total_ordens} OSs`
    })
  const exibirSucesso = (mensagem: string) => {
    setErro('')
    setSucesso(mensagem)
  }
  return { ocupado, sucesso, erro, inconsistencias, finalizar, gerarRpa, exibirSucesso }
}
