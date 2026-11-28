// Tempo para o navegador iniciar o download antes de liberar o objeto da memória.
const ESPERA_PARA_LIBERAR_MS = 1000

/** Entrega um Blob ao usuário como arquivo baixado, sem abrir nova aba. */
export function salvarArquivo(conteudo: Blob, nomeArquivo: string) {
  const endereco = URL.createObjectURL(conteudo)
  const link = document.createElement('a')
  link.href = endereco
  link.download = nomeArquivo
  // Revogar a URL logo após o clique cancela o download em alguns navegadores.
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.setTimeout(() => URL.revokeObjectURL(endereco), ESPERA_PARA_LIBERAR_MS)
}
