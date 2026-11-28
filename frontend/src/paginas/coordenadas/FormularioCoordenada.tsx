import { useState, type FormEvent } from 'react'
import { CircleMarker } from 'react-leaflet'
import { MapaBase } from '../../componentes/MapaBase'
import { MensagemErro } from '../../componentes/MensagemErro'
import { mensagemDeErro } from '../../servicos/cliente'
import { informarCoordenada } from '../../servicos/unidades'
import type { Unidade } from '../../tipos/api'
import type { Ponto } from '../../utilitarios/geometria'

const CASAS_DECIMAIS = 6

type Propriedades = { unidade: Unidade; aoSalvar: (unidade: Unidade) => void }

function paraNumero(texto: string): number | null {
  const valor = Number(texto.trim().replace(',', '.'))
  return texto.trim() && Number.isFinite(valor) ? valor : null
}

function useCoordenada(unidade: Unidade, aoSalvar: Propriedades['aoSalvar']) {
  const [latitude, setLatitude] = useState(unidade.latitude ?? '')
  const [longitude, setLongitude] = useState(unidade.longitude ?? '')
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)
  // HU-024 CA02: clicar no mapa preenche os campos para o usuário confirmar.
  const marcar = (ponto: Ponto) => {
    setLatitude(ponto.latitude.toFixed(CASAS_DECIMAIS).replace('.', ','))
    setLongitude(ponto.longitude.toFixed(CASAS_DECIMAIS).replace('.', ','))
  }
  const salvar = async (evento: FormEvent) => {
    evento.preventDefault()
    setEnviando(true)
    setErro('')
    try {
      aoSalvar(await informarCoordenada(unidade.id, latitude, longitude))
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }
  return { latitude, longitude, setLatitude, setLongitude, erro, enviando, marcar, salvar }
}

/** HU-024: digitar (vírgula ou ponto) ou clicar no mapa; o servidor valida a área (CA03). */
export function FormularioCoordenada({ unidade, aoSalvar }: Propriedades) {
  const estado = useCoordenada(unidade, aoSalvar)
  const lat = paraNumero(estado.latitude)
  const lng = paraNumero(estado.longitude)
  const ponto = lat !== null && lng !== null ? [{ latitude: lat, longitude: lng }] : []
  return (
    <section className="cartao" aria-labelledby="titulo-coordenada">
      <h2 id="titulo-coordenada">
        {unidade.codigo} · {unidade.nome}
      </h2>
      <form className="formulario-grade" onSubmit={estado.salvar}>
        <label className="campo">
          Latitude
          <input
            required
            inputMode="decimal"
            placeholder="-7,0832"
            value={estado.latitude}
            onChange={(e) => estado.setLatitude(e.target.value)}
          />
        </label>
        <label className="campo">
          Longitude
          <input
            required
            inputMode="decimal"
            placeholder="-34,8336"
            value={estado.longitude}
            onChange={(e) => estado.setLongitude(e.target.value)}
          />
        </label>
        <button type="submit" className="botao botao-primario" disabled={estado.enviando}>
          {estado.enviando ? 'Salvando…' : 'Salvar coordenada'}
        </button>
      </form>
      {estado.erro && <MensagemErro mensagem={estado.erro} />}
      <p className="texto-suave">Ou clique no mapa no ponto da unidade para preencher os campos.</p>
      <MapaBase
        rotulo="Mapa para marcar a coordenada da unidade"
        enquadrar={ponto}
        aoClicar={estado.marcar}
      >
        {ponto.map((p) => (
          <CircleMarker
            key="ponto"
            center={[p.latitude, p.longitude]}
            radius={10}
            pathOptions={{ color: '#047857' }}
          />
        ))}
      </MapaBase>
    </section>
  )
}
