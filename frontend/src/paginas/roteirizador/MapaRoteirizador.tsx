import { CircleMarker, Polygon, Polyline, Tooltip } from 'react-leaflet'
import { MapaBase } from '../../componentes/MapaBase'
import type { OrdemNoMapa, Rota } from '../../tipos/api'
import { agruparPorLocal, type LocalNoMapa } from '../../utilitarios/agrupamento'
import type { Ponto } from '../../utilitarios/geometria'

const COR_APTA = '#475569'
const COR_SELECIONADA = '#047857'
const COR_ROTA_PADRAO = '#7c3aed'

type Propriedades = {
  ordensAptas: OrdemNoMapa[]
  rotas: Rota[]
  estaSelecionada: (id: number) => boolean
  vertices: Ponto[]
  aoClicarNoMapa: (ponto: Ponto) => void
}

function raio(quantidade: number) {
  return Math.min(8 + quantidade * 1.5, 20)
}

function PinAptas({ local, selecionadas }: { local: LocalNoMapa; selecionadas: number }) {
  const total = local.ordens.length
  const cor = selecionadas ? COR_SELECIONADA : COR_APTA
  return (
    <CircleMarker
      center={[local.latitude, local.longitude]}
      radius={raio(total)}
      pathOptions={{ color: cor, fillColor: cor, fillOpacity: selecionadas ? 0.85 : 0.45 }}
    >
      <Tooltip>
        {local.unidade}: {total} OS(s) aptas{selecionadas ? ` · ${selecionadas} selecionadas` : ''}
      </Tooltip>
    </CircleMarker>
  )
}

function PinsDaRota({ rota }: { rota: Rota }) {
  const cor = rota.cor || COR_ROTA_PADRAO
  return agruparPorLocal(rota.ordens).map((local) => (
    <CircleMarker
      key={`${rota.id}-${local.chave}`}
      center={[local.latitude, local.longitude]}
      radius={raio(local.ordens.length)}
      pathOptions={{ color: cor, fillColor: cor, fillOpacity: 0.25, dashArray: '4' }}
    >
      <Tooltip>
        {rota.nome} · {local.unidade}: {local.ordens.length} OS(s)
      </Tooltip>
    </CircleMarker>
  ))
}

function Desenho({ vertices }: { vertices: Ponto[] }) {
  const posicoes = vertices.map((v) => [v.latitude, v.longitude] as [number, number])
  if (posicoes.length >= 3)
    return <Polygon positions={posicoes} pathOptions={{ color: COR_SELECIONADA, dashArray: '6' }} />
  return <Polyline positions={posicoes} pathOptions={{ color: COR_SELECIONADA }} />
}

/** HU-012: OSs aptas como pins (agrupados por unidade), rotas criadas e o polígono em desenho. */
export function MapaRoteirizador(props: Propriedades) {
  const locais = agruparPorLocal(props.ordensAptas)
  const pontos = [...props.ordensAptas, ...props.rotas.flatMap((rota) => rota.ordens)]
  return (
    <MapaBase
      rotulo="Mapa das OSs aptas a roteirizar"
      enquadrar={pontos}
      aoClicar={props.aoClicarNoMapa}
    >
      {props.rotas.map((rota) => (
        <PinsDaRota key={rota.id} rota={rota} />
      ))}
      {locais.map((local) => (
        <PinAptas
          key={local.chave}
          local={local}
          selecionadas={local.ordens.filter((o) => props.estaSelecionada(o.id)).length}
        />
      ))}
      {props.vertices.length > 0 && <Desenho vertices={props.vertices} />}
    </MapaBase>
  )
}
