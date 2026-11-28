import { useState, type FormEvent } from 'react'
import { Dialogo } from '../../componentes/Dialogo'
import { MensagemErro } from '../../componentes/MensagemErro'
import { mensagemDeErro } from '../../servicos/cliente'
import { criarRota } from '../../servicos/roteirizacao'
import type { ChavePlanejamento, Equipe, Rota } from '../../tipos/api'

type Propriedades = {
  chave: ChavePlanejamento
  ordensIds: number[]
  equipes: Equipe[]
  aoFechar: () => void
  aoCriar: (rota: Rota) => void
}

const CAMPOS_INICIAIS = {
  nome: '',
  equipeId: '',
  previsaoInicio: '07:30',
  carregamento: '07:00',
  cor: '#7c3aed',
  observacao: '',
}

function useFormularioRota(props: Propriedades) {
  const [campos, setCampos] = useState(CAMPOS_INICIAIS)
  const [enviando, setEnviando] = useState(false)
  const [erro, setErro] = useState('')
  const alterar = (parcial: Partial<Campos>) => setCampos((atual) => ({ ...atual, ...parcial }))
  const enviar = async (evento: FormEvent) => {
    evento.preventDefault()
    setEnviando(true)
    setErro('')
    try {
      const rota = await criarRota({
        ...props.chave,
        nome: campos.nome,
        equipe_id: Number(campos.equipeId),
        previsao_inicio: campos.previsaoInicio,
        carregamento: campos.carregamento,
        cor: campos.cor,
        observacao: campos.observacao,
        ordens_ids: props.ordensIds,
      })
      props.aoCriar(rota)
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }
  return { campos, alterar, enviando, erro, enviar }
}

type Campos = typeof CAMPOS_INICIAIS
type PropriedadesCampos = {
  campos: Campos
  equipes: Equipe[]
  alterar: (parcial: Partial<Campos>) => void
}

function CamposDaRota({ campos, equipes, alterar }: PropriedadesCampos) {
  return (
    <>
      <label className="campo">
        Nome da rota
        <input
          required
          maxLength={80}
          value={campos.nome}
          onChange={(e) => alterar({ nome: e.target.value })}
        />
      </label>
      <label className="campo">
        Equipe · veículo
        <select
          required
          value={campos.equipeId}
          onChange={(e) => alterar({ equipeId: e.target.value })}
        >
          <option value="">Selecione…</option>
          {equipes.map((equipe) => (
            <option key={equipe.id} value={equipe.id}>
              {`${equipe.nome} · ${equipe.placa || 'sem placa'} (capacidade ${equipe.capacidade_diaria})`}
            </option>
          ))}
        </select>
      </label>
      <HorariosDaRota campos={campos} alterar={alterar} />
      <label className="campo">
        Cor no mapa
        <input type="color" value={campos.cor} onChange={(e) => alterar({ cor: e.target.value })} />
      </label>
      <label className="campo">
        Observação (opcional)
        <input
          maxLength={500}
          value={campos.observacao}
          onChange={(e) => alterar({ observacao: e.target.value })}
        />
      </label>
    </>
  )
}

function HorariosDaRota({ campos, alterar }: Omit<PropriedadesCampos, 'equipes'>) {
  return (
    <>
      <label className="campo">
        Previsão de início
        <input
          type="time"
          required
          value={campos.previsaoInicio}
          onChange={(e) => alterar({ previsaoInicio: e.target.value })}
        />
      </label>
      <label className="campo">
        Carregamento
        <input
          type="time"
          required
          value={campos.carregamento}
          onChange={(e) => alterar({ carregamento: e.target.value })}
        />
      </label>
    </>
  )
}

/** HU-056: modal "Criar Rota". O servidor revalida equipe, capacidade e cada OS. */
export function DialogoCriarRota(props: Propriedades) {
  const { campos, alterar, enviando, erro, enviar } = useFormularioRota(props)
  return (
    <Dialogo titulo={`Criar rota com ${props.ordensIds.length} OSs`} aoFechar={props.aoFechar}>
      <form className="formulario-grade" onSubmit={enviar}>
        <CamposDaRota campos={campos} equipes={props.equipes} alterar={alterar} />
        {erro && <MensagemErro mensagem={erro} />}
        <div className="barra-acoes">
          <button type="button" className="botao" onClick={props.aoFechar}>
            Cancelar
          </button>
          <button type="submit" className="botao botao-primario" disabled={enviando}>
            {enviando ? 'Salvando…' : 'Salvar rota'}
          </button>
        </div>
      </form>
    </Dialogo>
  )
}
