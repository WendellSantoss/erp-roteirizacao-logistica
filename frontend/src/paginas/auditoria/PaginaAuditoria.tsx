import { useCallback } from 'react'
import { EstadoDaConsulta } from '../../componentes/EstadoDaConsulta'
import { ListaVazia } from '../../componentes/ListaVazia'
import { TituloPagina } from '../../componentes/TituloPagina'
import { useConsulta } from '../../hooks/useConsulta'
import { listarAuditoria } from '../../servicos/auditoria'
import type { RegistroAuditoria } from '../../tipos/api'
import { formatarDataHora } from '../../utilitarios/formatacao'

function valorLegivel(valor: unknown): string {
  if (valor === null || valor === undefined) return '—'
  return typeof valor === 'object' ? JSON.stringify(valor) : String(valor)
}

function TabelaAuditoria({ registros }: { registros: RegistroAuditoria[] }) {
  if (registros.length === 0)
    return <ListaVazia titulo="Nenhum registro na trilha para os polos selecionados" />
  return (
    <div className="tabela-rolagem">
      <table className="tabela">
        <caption className="oculto-visualmente">Trilha de auditoria</caption>
        <thead>
          <tr>
            {['Quando', 'Autor', 'Entidade', 'Campo', 'Antes', 'Depois', 'Justificativa'].map(
              (c) => (
                <th scope="col" key={c}>
                  {c}
                </th>
              ),
            )}
          </tr>
        </thead>
        <tbody>
          {registros.map((registro) => (
            <tr key={registro.id}>
              <td className="mono">{formatarDataHora(registro.registrado_em)}</td>
              <td>{registro.autor}</td>
              <td>{`${registro.entidade}${registro.entidade_id ? ` #${registro.entidade_id}` : ''}`}</td>
              <td>{registro.campo}</td>
              <td className="mono">{valorLegivel(registro.valor_anterior)}</td>
              <td className="mono">{valorLegivel(registro.valor_novo)}</td>
              <td style={{ whiteSpace: 'normal', minWidth: 240 }}>
                {registro.justificativa || '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

/** HU-045 (consulta): trilha imutável das alterações manuais e tentativas bloqueadas. */
export function PaginaAuditoria() {
  const carregar = useCallback(() => listarAuditoria(), [])
  const consulta = useConsulta(carregar)
  return (
    <>
      <TituloPagina
        titulo="Trilha de auditoria"
        subtitulo="Registros imutáveis: prioridade, desconsideração e saídas de kit bloqueadas."
      />
      <EstadoDaConsulta consulta={consulta}>
        {(dados) => <TabelaAuditoria registros={dados.resultados} />}
      </EstadoDaConsulta>
    </>
  )
}
