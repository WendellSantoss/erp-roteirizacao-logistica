import { useEffect, type ComponentType } from 'react'
import { Carregando } from './componentes/Carregando'
import { Leiaute } from './componentes/Leiaute'
import { ProvedorSessao } from './componentes/ProvedorSessao'
import { useSessao } from './hooks/contextoSessao'
import { navegar, useRota } from './hooks/useRota'
import { PaginaAlmoxarifado } from './paginas/almoxarifado/PaginaAlmoxarifado'
import { PaginaAuditoria } from './paginas/auditoria/PaginaAuditoria'
import { PaginaImportacao } from './paginas/importacao/PaginaImportacao'
import { PaginaLogin } from './paginas/login/PaginaLogin'
import { PaginaPendencias } from './paginas/pendencias/PaginaPendencias'
import { PaginaSemAcesso } from './paginas/PaginaSemAcesso'
import { PaginaStatus } from './paginas/status/PaginaStatus'
import { ITENS_MENU } from './utilitarios/menu'

const COMPONENTES: Record<string, ComponentType> = {
  '/pendencias': PaginaPendencias,
  '/importacao': PaginaImportacao,
  '/almoxarifado': PaginaAlmoxarifado,
  '/auditoria': PaginaAuditoria,
}

function Redirecionar({ para }: { para: string }) {
  useEffect(() => navegar(para, true), [para])
  return null
}

function PaginaAutenticada({ rota }: { rota: string }) {
  const { polo, podeVer } = useSessao()
  const item = ITENS_MENU.find((opcao) => opcao.caminho === rota)
  const primeira = ITENS_MENU.find((opcao) => podeVer(opcao.modulo))
  if (!item) return <Redirecionar para={primeira?.caminho ?? '/pendencias'} />
  const Componente = COMPONENTES[item.caminho]
  return (
    <Leiaute titulo={item.rotulo}>
      {/* HU-020 CA04: a URL de uma área proibida mostra o aviso; a API também responde 403. */}
      {podeVer(item.modulo) ? <Componente key={polo} /> : <PaginaSemAcesso />}
    </Leiaute>
  )
}

function Roteador() {
  const { usuario, verificando } = useSessao()
  const rota = useRota()
  if (rota === '/status') return <PaginaStatus />
  if (verificando) return <Carregando texto="Verificando sua sessão…" />
  // HU-019 CA04: a URL não muda no login, então o usuário volta à tela onde estava.
  if (!usuario) return <PaginaLogin />
  return <PaginaAutenticada rota={rota} />
}

export function App() {
  return (
    <ProvedorSessao>
      <Roteador />
    </ProvedorSessao>
  )
}

export default App
