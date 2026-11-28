// Guarda token e polo selecionado no navegador. O token fica em sessionStorage: some ao fechar
// a aba. O polo fica em localStorage para o seletor persistir entre sessões (histórias priorizadas §1).

const CHAVE_TOKEN = 'genios.token'
const CHAVE_POLO = 'genios.polo'

function ler(armazenamento: Storage, chave: string): string | null {
  try {
    return armazenamento.getItem(chave)
  } catch {
    return null
  }
}

function gravar(armazenamento: Storage, chave: string, valor: string | null) {
  try {
    if (valor === null) armazenamento.removeItem(chave)
    else armazenamento.setItem(chave, valor)
  } catch {
    // Navegação privada ou armazenamento bloqueado: a sessão vale só enquanto a página está aberta.
  }
}

export const lerToken = () => ler(sessionStorage, CHAVE_TOKEN)
export const gravarToken = (token: string | null) => gravar(sessionStorage, CHAVE_TOKEN, token)
export const lerPolo = () => ler(localStorage, CHAVE_POLO)
export const gravarPolo = (polo: string) => gravar(localStorage, CHAVE_POLO, polo)

// HU-011 CA04: a operação e a data escolhidas no Roteirizador valem para a sessão inteira.
const CHAVE_PLANEJAMENTO = 'genios.planejamento'
export const lerPlanejamento = () => ler(sessionStorage, CHAVE_PLANEJAMENTO)
export const gravarPlanejamento = (valor: string) =>
  gravar(sessionStorage, CHAVE_PLANEJAMENTO, valor)
