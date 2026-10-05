#!/usr/bin/env python3
"""Gera o índice e a rastreabilidade das histórias e confere a consistência.

Uso: python3 scripts/historias.py          # regenera os arquivos
     python3 scripts/historias.py --check  # só confere (falha com código 1)
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HISTORIAS = RAIZ / "docs" / "historias"
ERS = RAIZ / "docs" / "requisitos" / "ers.md"
INDICE_INICIO = "<!-- indice:inicio -->"
INDICE_FIM = "<!-- indice:fim -->"

EPICOS = [
    "EP-0 Fundação técnica",
    "EP-A Ingestão e preparação de dados",
    "EP-B Planejamento e despacho",
    "EP-C Suprimentos e logística",
    "EP-D Fechamento, auditoria e faturamento",
    "EP-E Inteligência e suporte à decisão",
    "EP-F Requisitos transversais",
]


def ler_cabecalho(caminho):
    texto = caminho.read_text(encoding="utf-8")
    bloco = re.match(r"---\n(.*?)\n---", texto, re.S).group(1)
    dados = {}
    for linha in bloco.splitlines():
        chave, _, valor = linha.partition(":")
        valor = valor.strip()
        if valor.startswith("["):
            valor = [v.strip() for v in valor[1:-1].split(",") if v.strip()]
        dados[chave.strip()] = valor
    dados["arquivo"] = caminho.relative_to(HISTORIAS).as_posix()
    return dados


def chave_ordem(h):
    i = h["id"]
    return (0, int(i[4:])) if i.startswith("HU-F") else (1, int(i[3:]))


def ids_da_ers(prefixo):
    return sorted(set(re.findall(rf"\*\*({prefixo}-[A-Z]*-?\d+)", ERS.read_text(encoding="utf-8"))))


def so_id(ref):
    return ref.split(" ")[0]


def main():
    historias = sorted(
        (ler_cabecalho(p) for p in HISTORIAS.rglob("HU-*.md")), key=chave_ordem
    )
    ids = {h["id"] for h in historias}
    erros = []

    for h in historias:
        for dep in h["depende_de"]:
            if dep not in ids:
                erros.append(f"{h['id']}: depende de {dep}, que não existe")
        if h["epico"] not in EPICOS:
            erros.append(f"{h['id']}: épico desconhecido '{h['epico']}'")

    rf_cobertos = {so_id(r): [] for h in historias for r in h["requisitos"]}
    rn_cobertas = {r: [] for h in historias for r in h["regras"]}
    rnf_cobertos = {r: [] for h in historias for r in h["nao_funcionais"]}
    for h in historias:
        for r in h["requisitos"]:
            rf_cobertos[so_id(r)].append(h["id"])
        for r in h["regras"]:
            rn_cobertas[r].append(h["id"])
        for r in h["nao_funcionais"]:
            rnf_cobertos[r].append(h["id"])

    rfs_ers = ids_da_ers("RF")
    rns_ers = ids_da_ers("RN")
    rnfs_ers = ids_da_ers("RNF")
    for rf in rfs_ers:
        if rf not in rf_cobertos:
            erros.append(f"{rf} da ERS não tem história")

    if "--check" in sys.argv:
        for e in erros:
            print("ERRO:", e)
        print(f"{len(historias)} histórias, {len(erros)} erros")
        sys.exit(1 if erros else 0)

    # Índice no README, agrupado por épico
    linhas = [INDICE_INICIO, ""]
    for ep in EPICOS:
        do_epico = [h for h in historias if h["epico"] == ep]
        linhas += [f"### {ep} ({len(do_epico)})", "",
                   "| ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |",
                   "|---|---|---|---|---|---|---|"]
        for h in do_epico:
            linhas.append(
                f"| [{h['id']}]({h['arquivo']}) | {h['titulo']} | {h['fase']} | {h['prioridade']} "
                f"| {h['status']} | {', '.join(h['requisitos']) or '—'} | {', '.join(h['depende_de']) or '—'} |"
            )
        linhas.append("")
    linhas.append(INDICE_FIM)
    readme = HISTORIAS / "README.md"
    texto = readme.read_text(encoding="utf-8")
    texto = re.sub(rf"{INDICE_INICIO}.*{INDICE_FIM}", "\n".join(linhas), texto, flags=re.S)
    readme.write_text(texto, encoding="utf-8")

    # Matriz de rastreabilidade
    def tabela(titulo, ers_ids, cobertos, extra):
        out = [f"## {titulo}", "", "| Item | Histórias |", "|---|---|"]
        for i in ers_ids:
            out.append(f"| {i} | {', '.join(cobertos.get(i, [])) or '**sem história**'} |")
        for i in sorted(set(cobertos) - set(ers_ids)):
            out.append(f"| {i} *{extra}* | {', '.join(cobertos[i])} |")
        return out + [""]

    rastro = [
        "# Rastreabilidade ERS ↔ histórias",
        "",
        "> Gerado por `scripts/historias.py` a partir dos cabeçalhos das histórias. Não editar à mão.",
        "",
        f"- Histórias: {len(historias)} "
        f"({sum(h['status'] == 'proposta' for h in historias)} propostas, "
        f"{sum(h['id'].startswith('HU-F') for h in historias)} de fundação)",
        f"- RFs da ERS cobertos: {sum(r in rf_cobertos for r in rfs_ers)} de {len(rfs_ers)}",
        f"- RNs da ERS citadas: {sum(r in rn_cobertas for r in rns_ers)} de {len(rns_ers)}",
        f"- RNFs da ERS verificados por alguma história: {sum(r in rnf_cobertos for r in rnfs_ers)} de {len(rnfs_ers)}",
        "",
    ]
    rastro += tabela("Requisitos funcionais", rfs_ers, rf_cobertos, "(proposto)")
    rastro += tabela("Regras de negócio", rns_ers, rn_cobertas, "")
    rastro += tabela("Requisitos não funcionais", rnfs_ers, rnf_cobertos, "")
    (HISTORIAS / "RASTREABILIDADE.md").write_text("\n".join(rastro), encoding="utf-8")

    for e in erros:
        print("ERRO:", e)
    print(f"{len(historias)} histórias, {len(erros)} erros")


if __name__ == "__main__":
    main()
