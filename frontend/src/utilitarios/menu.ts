import type { Modulo } from '../tipos/api'

/** Telas do MVP e o módulo da matriz de acesso (HU-020) que cada uma exige. */
export const ITENS_MENU: { modulo: Modulo; caminho: string; rotulo: string }[] = [
  { modulo: 'pendencias', caminho: '/pendencias', rotulo: 'Pendências' },
  { modulo: 'importacao', caminho: '/importacao', rotulo: 'Importação' },
  { modulo: 'almoxarifado', caminho: '/almoxarifado', rotulo: 'Almoxarifado' },
  { modulo: 'auditoria', caminho: '/auditoria', rotulo: 'Auditoria' },
]
