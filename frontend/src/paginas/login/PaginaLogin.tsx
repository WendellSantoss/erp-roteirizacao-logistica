import { useState, type FormEvent } from 'react'
import { MensagemErro } from '../../componentes/MensagemErro'
import { useSessao } from '../../hooks/contextoSessao'
import { entrar } from '../../servicos/autenticacao'
import { mensagemDeErro } from '../../servicos/cliente'

function useEnvioDoLogin() {
  const { concluirLogin } = useSessao()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [erro, setErro] = useState('')

  const aoEnviar = async (evento: FormEvent) => {
    evento.preventDefault()
    setEnviando(true)
    setErro('')
    try {
      const resposta = await entrar(email, senha)
      concluirLogin(resposta.access_token, resposta.usuario)
    } catch (falha) {
      setErro(mensagemDeErro(falha))
    } finally {
      setEnviando(false)
    }
  }
  return { email, setEmail, senha, setSenha, enviando, erro, aoEnviar }
}

/** HU-019: login individual por e-mail e senha. */
export function PaginaLogin() {
  const { aviso } = useSessao()
  const { email, setEmail, senha, setSenha, enviando, erro, aoEnviar } = useEnvioDoLogin()
  return (
    <main className="tela-login">
      <form className="cartao cartao-login" onSubmit={aoEnviar} aria-describedby="ajuda-login">
        <div>
          <h1>GeniOS</h1>
          <p className="texto-suave" id="ajuda-login" style={{ margin: '4px 0 0' }}>
            Entre com seu usuário individual.
          </p>
        </div>
        {aviso && (
          <div className="aviso aviso-alerta" role="status">
            {aviso}
          </div>
        )}
        <label className="campo">
          E-mail
          <input
            type="email"
            autoComplete="username"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="campo">
          Senha
          <input
            type="password"
            autoComplete="current-password"
            required
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />
        </label>
        {erro && <MensagemErro mensagem={erro} />}
        <button type="submit" className="botao botao-primario" disabled={enviando}>
          {enviando ? 'Entrando… (pode levar até 1 min se o servidor hibernou)' : 'Entrar'}
        </button>
      </form>
    </main>
  )
}
