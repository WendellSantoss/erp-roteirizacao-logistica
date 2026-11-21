import { useId, useState, type DragEvent } from 'react'

type Propriedades = {
  desabilitada: boolean
  enviando: boolean
  aoEscolher: (arquivos: File[]) => void
}

/** HU-001 CA01/CA02/CA06: seleção ou arrastar e soltar; desabilitada com o polo "Todos". */
export function AreaEnvio({ desabilitada, enviando, aoEscolher }: Propriedades) {
  const idEntrada = useId()
  const [arrastando, setArrastando] = useState(false)
  const bloqueada = desabilitada || enviando

  const aoSoltar = (evento: DragEvent) => {
    evento.preventDefault()
    setArrastando(false)
    if (!bloqueada) aoEscolher(Array.from(evento.dataTransfer.files))
  }
  const aoArrastar = (evento: DragEvent) => {
    evento.preventDefault()
    if (!bloqueada) setArrastando(true)
  }

  return (
    <div
      className={`area-envio${arrastando ? ' arrastando' : ''}`}
      aria-disabled={bloqueada}
      onDragOver={aoArrastar}
      onDragLeave={() => setArrastando(false)}
      onDrop={aoSoltar}
    >
      <p style={{ fontWeight: 700, marginTop: 0 }}>
        {desabilitada
          ? 'Selecione um polo para importar'
          : 'Arraste a planilha do GSAN (.xlsx) para cá'}
      </p>
      <input
        id={idEntrada}
        className="oculto-visualmente"
        type="file"
        accept=".xlsx"
        disabled={bloqueada}
        onChange={(evento) => {
          aoEscolher(Array.from(evento.target.files ?? []))
          evento.target.value = ''
        }}
      />
      <label
        htmlFor={idEntrada}
        className="botao botao-primario"
        aria-disabled={bloqueada}
        style={{ display: 'inline-block' }}
      >
        {enviando ? 'Importando…' : 'Selecionar arquivo'}
      </label>
      <p className="texto-suave" style={{ marginBottom: 0 }}>
        Um arquivo por vez, até 25 MB.
      </p>
    </div>
  )
}
