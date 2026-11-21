import { useState, type FormEvent } from 'react'
import type { Equipe, LimiteKit, PedidoSaidaKit } from '../../tipos/api'

type Propriedades = {
  equipes: Equipe[]
  kits: LimiteKit[]
  enviando: boolean
  aoRegistrar: (pedido: PedidoSaidaKit) => Promise<boolean>
}

/** Saída de kit para uma equipe; a trava é aplicada no servidor (RNF-08). */
export function FormularioSaida({ equipes, kits, enviando, aoRegistrar }: Propriedades) {
  const [equipeId, setEquipeId] = useState('')
  const [kitId, setKitId] = useState('')
  const [quantidade, setQuantidade] = useState('1')

  const aoEnviar = async (evento: FormEvent) => {
    evento.preventDefault()
    const pedido = {
      equipe_id: Number(equipeId),
      kit_id: Number(kitId),
      quantidade: Number(quantidade),
    }
    if (await aoRegistrar(pedido)) setQuantidade('1')
  }

  return (
    <form
      className="cartao formulario-grade"
      onSubmit={aoEnviar}
      aria-label="Registrar saída de kit"
    >
      <label className="campo">
        Equipe
        <select required value={equipeId} onChange={(e) => setEquipeId(e.target.value)}>
          <option value="">Selecione…</option>
          {equipes.map((equipe) => (
            <option key={equipe.id} value={equipe.id}>{`${equipe.codigo} (${equipe.nome})`}</option>
          ))}
        </select>
      </label>
      <label className="campo">
        Tipo de kit
        <select required value={kitId} onChange={(e) => setKitId(e.target.value)}>
          <option value="">Selecione…</option>
          {kits.map((kit) => (
            <option key={kit.kit_id} value={kit.kit_id}>
              {kit.nome}
            </option>
          ))}
        </select>
      </label>
      <label className="campo">
        Quantidade
        <input
          type="number"
          min={1}
          step={1}
          required
          value={quantidade}
          onChange={(e) => setQuantidade(e.target.value)}
        />
      </label>
      <button type="submit" className="botao botao-primario" disabled={enviando}>
        {enviando ? 'Registrando…' : 'Registrar saída'}
      </button>
    </form>
  )
}
