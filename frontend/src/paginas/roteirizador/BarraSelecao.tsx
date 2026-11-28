type Propriedades = {
  quantidade: number
  capacidadeMaxima: number
  podeCriar: boolean
  aoLimpar: () => void
  aoCriarRota: () => void
}

/** HU-031: contador, limpar e comparação com a maior capacidade das equipes do polo. */
export function BarraSelecao({ quantidade, capacidadeMaxima, podeCriar, ...acoes }: Propriedades) {
  const acimaDaCapacidade = capacidadeMaxima > 0 && quantidade > capacidadeMaxima
  return (
    <div className="cartao barra-selecao">
      <strong aria-live="polite">
        {quantidade} {quantidade === 1 ? 'OS selecionada' : 'OSs selecionadas'}
      </strong>
      {acimaDaCapacidade && (
        <span className="selo selo-vencendo" role="status">
          Acima da capacidade de qualquer equipe do polo (máx. {capacidadeMaxima})
        </span>
      )}
      <div className="barra-acoes">
        <button
          type="button"
          className="botao"
          disabled={quantidade === 0}
          onClick={acoes.aoLimpar}
        >
          Limpar
        </button>
        <button
          type="button"
          className="botao botao-primario"
          disabled={quantidade === 0 || !podeCriar}
          onClick={acoes.aoCriarRota}
        >
          Criar Rota
        </button>
      </div>
    </div>
  )
}
