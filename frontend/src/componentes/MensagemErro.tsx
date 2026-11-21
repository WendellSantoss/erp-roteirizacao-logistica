type Propriedades = { mensagem: string; aoTentarDeNovo?: () => void }

export function MensagemErro({ mensagem, aoTentarDeNovo }: Propriedades) {
  return (
    <div className="aviso aviso-erro" role="alert">
      <p style={{ margin: 0 }}>{mensagem}</p>
      {aoTentarDeNovo && (
        <button
          type="button"
          className="botao botao-pequeno"
          onClick={aoTentarDeNovo}
          style={{ marginTop: 8 }}
        >
          Tentar de novo
        </button>
      )}
    </div>
  )
}
