// HU-001: a tela recusa antes do upload; o servidor repete a validação (CA05).
const LIMITE_BYTES = 25 * 1024 * 1024
const BYTES_POR_MB = 1024 * 1024

/** Devolve a mensagem de recusa ou string vazia quando o envio pode seguir. */
export function motivoDeRecusa(arquivos: File[]): string {
  if (arquivos.length === 0) return ''
  if (arquivos.length > 1) return 'Envie um arquivo por vez'
  const [arquivo] = arquivos
  if (!arquivo.name.toLowerCase().endsWith('.xlsx'))
    return 'Formato não aceito: envie a planilha do GSAN em .xlsx'
  if (arquivo.size > LIMITE_BYTES) {
    return `Arquivo com ${Math.round(arquivo.size / BYTES_POR_MB)} MB excede o limite de 25 MB`
  }
  return ''
}
