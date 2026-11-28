import 'leaflet/dist/leaflet.css'
import { useEffect, type ReactNode } from 'react'
import { MapContainer, TileLayer, useMap, useMapEvents } from 'react-leaflet'
import type { Ponto } from '../utilitarios/geometria'

// Centro de João Pessoa: abertura do mapa antes de haver pontos (área da HU-005 RN-L02).
const CENTRO_PADRAO: [number, number] = [-7.12, -34.86]
const ZOOM_PADRAO = 12
const ZOOM_MAXIMO_AO_ENQUADRAR = 15

function Enquadrar({ pontos }: { pontos: Ponto[] }) {
  const mapa = useMap()
  const assinatura = pontos.map((p) => `${p.latitude},${p.longitude}`).join('|')
  useEffect(() => {
    if (!pontos.length) return
    const limites = pontos.map((p) => [p.latitude, p.longitude] as [number, number])
    mapa.fitBounds(limites, { padding: [32, 32], maxZoom: ZOOM_MAXIMO_AO_ENQUADRAR })
    // A assinatura evita reenquadrar a cada render quando os pontos não mudaram.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mapa, assinatura])
  return null
}

function OuvirCliques({ aoClicar }: { aoClicar?: (ponto: Ponto) => void }) {
  useMapEvents({
    click: (evento) => aoClicar?.({ latitude: evento.latlng.lat, longitude: evento.latlng.lng }),
  })
  return null
}

type Propriedades = {
  rotulo: string
  enquadrar: Ponto[]
  aoClicar?: (ponto: Ponto) => void
  children?: ReactNode
}

/** Mapa OpenStreetMap com enquadramento automático (ADR-002). */
export function MapaBase({ rotulo, enquadrar, aoClicar, children }: Propriedades) {
  return (
    <div className="mapa" role="region" aria-label={rotulo}>
      <MapContainer center={CENTRO_PADRAO} zoom={ZOOM_PADRAO} className="mapa-leaflet">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Enquadrar pontos={enquadrar} />
        <OuvirCliques aoClicar={aoClicar} />
        {children}
      </MapContainer>
    </div>
  )
}
