import type { OrdemServico } from '../../tipos/api'
import { LinhaOrdemServico, type AcoesDaLinha } from './LinhaOrdemServico'

const COLUNAS = [
  'Especificação',
  'Tipo',
  'Nº do Imóvel',
  'Unidade Atual',
  'Cidade',
  'Setor',
  'Quadra',
  'Longitude',
  'Latitude',
  'Prazo (h)',
  'Abertura',
  'Decorrido',
  'Atraso',
  'Equipe',
  'Prioridade',
  'Ações',
]

type Propriedades = { ordens: OrdemServico[]; acoes: AcoesDaLinha }

export function TabelaOrdensServico({ ordens, acoes }: Propriedades) {
  return (
    <div className="tabela-rolagem">
      <table className="tabela">
        <caption className="oculto-visualmente">Ordens de serviço do filtro selecionado</caption>
        <thead>
          <tr>
            {acoes.marcacao && (
              <th scope="col">
                <span className="oculto-visualmente">Marcar</span>
              </th>
            )}
            <th scope="col" className="coluna-fixa">
              Ordem de Serviço
            </th>
            {acoes.mostrarPolo && <th scope="col">Polo</th>}
            {COLUNAS.map((coluna) => (
              <th scope="col" key={coluna}>
                {coluna}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {ordens.map((ordem) => (
            <LinhaOrdemServico key={ordem.id} ordem={ordem} acoes={acoes} />
          ))}
        </tbody>
      </table>
    </div>
  )
}
