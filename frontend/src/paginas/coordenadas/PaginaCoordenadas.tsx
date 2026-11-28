import { useCallback, useState } from 'react'
import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { ListaVazia } from '../../componentes/ListaVazia'
import { TituloPagina } from '../../componentes/TituloPagina'
import { useSessao } from '../../hooks/contextoSessao'
import { useConsulta } from '../../hooks/useConsulta'
import { POLO_TODOS } from '../../servicos/cliente'
import { listarUnidades } from '../../servicos/unidades'
import type { Unidade } from '../../tipos/api'
import { formatarCoordenada } from '../../utilitarios/formatacao'
import { FormularioCoordenada } from './FormularioCoordenada'

type PropriedadesTabela = {
  unidades: Unidade[]
  podeEditar: boolean
  aoEscolher: (unidade: Unidade) => void
}

function OrigemCoordenada({ unidade }: { unidade: Unidade }) {
  if (unidade.latitude === null) return <span className="selo selo-vencendo">Sem coordenada</span>
  // HU-024 RN-L02: a manual não é sobrescrita por captura automática.
  return <>{unidade.coordenada_manual ? 'Manual' : 'Captura'}</>
}

function TabelaUnidades({ unidades, podeEditar, aoEscolher }: PropriedadesTabela) {
  if (!unidades.length)
    return (
      <ListaVazia titulo="Todas as unidades têm coordenada">
        Nada a resolver neste filtro.
      </ListaVazia>
    )
  return (
    <div className="tabela-rolagem">
      <table className="tabela">
        <caption className="oculto-visualmente">Unidades e coordenadas</caption>
        <thead>
          <tr>
            {['Unidade', 'Polo', 'OSs', 'Latitude', 'Longitude', 'Origem', 'Ação'].map((c) => (
              <th scope="col" key={c}>
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {unidades.map((unidade) => (
            <tr key={unidade.id}>
              <th scope="row">{`${unidade.codigo} · ${unidade.nome}`}</th>
              <td>{unidade.polo}</td>
              <td className="mono">{unidade.total_ordens}</td>
              <td className="mono">
                {formatarCoordenada(unidade.latitude === null ? null : Number(unidade.latitude))}
              </td>
              <td className="mono">
                {formatarCoordenada(unidade.longitude === null ? null : Number(unidade.longitude))}
              </td>
              <td>
                <OrigemCoordenada unidade={unidade} />
              </td>
              <td>
                {podeEditar && (
                  <button
                    type="button"
                    className="botao botao-pequeno"
                    onClick={() => aoEscolher(unidade)}
                  >
                    Informar
                    <span className="oculto-visualmente"> coordenada de {unidade.nome}</span>
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

/** HU-024: coordenada manual das unidades que a captura não resolveu. */
export function PaginaCoordenadas() {
  const { polo, podeEditar } = useSessao()
  const [somenteSem, setSomenteSem] = useState(true)
  const [escolhida, setEscolhida] = useState<Unidade | null>(null)
  const [sucesso, setSucesso] = useState('')
  const carregar = useCallback(() => listarUnidades(somenteSem), [somenteSem])
  const consulta = useConsulta(carregar)
  const podeInformar = podeEditar('webscraper') && polo !== POLO_TODOS
  const aoSalvar = (unidade: Unidade) => {
    setEscolhida(null)
    setSucesso(`Coordenada de ${unidade.nome} salva. As OSs dela já podem ser liberadas.`)
    consulta.recarregar()
  }
  return (
    <>
      <TituloPagina
        titulo="Coordenadas das unidades"
        subtitulo="Sem coordenada válida a OS não vai para o mapa (RN-04)."
      />
      {podeEditar('webscraper') && polo === POLO_TODOS && (
        <div className="aviso aviso-info">
          Selecione um polo no cabeçalho para informar coordenadas.
        </div>
      )}
      <label className="campo-linha">
        <input
          type="checkbox"
          checked={somenteSem}
          onChange={(e) => setSomenteSem(e.target.checked)}
        />
        Mostrar só unidades sem coordenada
      </label>
      {sucesso && (
        <div className="aviso aviso-info" role="status">
          {sucesso}
        </div>
      )}
      <EstadoDaConsulta consulta={consulta}>
        {(dados) => (
          <TabelaUnidades
            unidades={dados.resultados}
            podeEditar={podeInformar}
            aoEscolher={setEscolhida}
          />
        )}
      </EstadoDaConsulta>
      {escolhida && (
        <FormularioCoordenada key={escolhida.id} unidade={escolhida} aoSalvar={aoSalvar} />
      )}
    </>
  )
}
