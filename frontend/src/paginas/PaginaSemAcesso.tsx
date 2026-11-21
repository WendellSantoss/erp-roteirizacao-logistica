import { ListaVazia } from '../componentes/ListaVazia'

/** HU-020 CA04: URL de uma área que o perfil não pode abrir. */
export function PaginaSemAcesso() {
  return (
    <div className="cartao">
      <ListaVazia titulo="Você não tem acesso a esta área">
        Use o menu para abrir as telas do seu perfil.
      </ListaVazia>
    </div>
  )
}
