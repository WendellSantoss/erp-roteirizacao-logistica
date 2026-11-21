import type { OrdemServico } from '../../tipos/api'
import { formatarHoras } from '../../utilitarios/formatacao'

const JANELA_VENCENDO_HORAS = 4 // HU-008 RN-L03

/** Faixas da HU-008: em atraso (vermelho), vence em até 4 h (amarelo) e no prazo. */
export function SeloAtraso({ ordem }: { ordem: OrdemServico }) {
  if (ordem.em_atraso)
    return <span className="selo selo-atraso">{formatarHoras(ordem.atraso_horas)}</span>
  if (ordem.atraso_horas >= -JANELA_VENCENDO_HORAS) {
    return <span className="selo selo-vencendo">vence em {formatarHoras(ordem.atraso_horas)}</span>
  }
  return <span className="texto-suave">—</span>
}
