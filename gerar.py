#!/usr/bin/env python3
"""Gera index.html e README.md a partir de catalogo.json.

    python gerar.py              # regenera os dois arquivos
    python gerar.py --verificar  # falha se estiverem desatualizados (usado no CI)

Só usa a biblioteca padrão. Nunca edite index.html nem README.md à mão:
edite catalogo.json e rode este script.
"""
from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CATALOGO = RAIZ / "catalogo.json"

OBRIGATORIOS = ["slug", "titulo", "subtitulo", "tipo", "versao", "publicado_em",
                "coautoria_ia", "numeros", "paginas", "repo", "site", "pdf"]

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def mes_ano(aaaa_mm: str) -> str:
    ano, mes = aaaa_mm.split("-")
    return f"{MESES[int(mes) - 1]} de {ano}"


def juntar(nomes: list[str]) -> str:
    if len(nomes) <= 1:
        return "".join(nomes)
    return ", ".join(nomes[:-1]) + " e " + nomes[-1]


def carregar() -> dict:
    dados = json.loads(CATALOGO.read_text(encoding="utf-8"))
    erros = []
    slugs = set()
    for i, eb in enumerate(dados["ebooks"]):
        faltando = [c for c in OBRIGATORIOS if not eb.get(c)]
        if faltando:
            erros.append(f"ebook #{i + 1} ({eb.get('slug', '?')}): faltam {', '.join(faltando)}")
        if eb.get("slug") in slugs:
            erros.append(f"slug repetido: {eb['slug']}")
        slugs.add(eb.get("slug"))
        capa = eb.get("capa")
        if capa and not (RAIZ / capa).exists():
            erros.append(f"{eb.get('slug')}: capa não encontrada em {capa}")
        try:
            mes_ano(eb.get("publicado_em", ""))
        except (ValueError, IndexError):
            erros.append(f"{eb.get('slug')}: publicado_em deve ser AAAA-MM")
    if erros:
        sys.exit("catalogo.json inválido:\n  - " + "\n  - ".join(erros))
    dados["ebooks"].sort(key=lambda e: e["publicado_em"], reverse=True)
    return dados


def url_repo(dados: dict, repo: str) -> str:
    return f"https://github.com/{dados['github']}/{repo}"


def url_pdf(dados: dict, eb: dict) -> str:
    return f"{url_repo(dados, eb['repo'])}/raw/main/{eb['pdf']}"


# ---------------------------------------------------------------- HTML

CSS = """
:root{
  --paper:#FFFEFC;--card:#FFFFFF;--ink:#17191C;--ink-soft:#3F444B;--muted:#6F6961;
  --rule:#E8E3DA;--accent:#C2410C;--accent-ink:#9A3412;--accent-soft:#FDF3EC;--accent-line:#F0D4C2;
  --cover-bg:#17191C;--shadow:0 1px 2px rgba(23,25,28,.06),0 8px 24px rgba(23,25,28,.07);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#121417;--card:#1A1D21;--ink:#F2EFE9;--ink-soft:#CFC9BC;--muted:#9C968B;
  --rule:#2C3036;--accent:#F0915A;--accent-ink:#F5A877;--accent-soft:#2A1E17;--accent-line:#4A2E1F;
  --cover-bg:#0B0C0E;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.25);
}}
:root[data-theme="dark"]{
  --paper:#121417;--card:#1A1D21;--ink:#F2EFE9;--ink-soft:#CFC9BC;--muted:#9C968B;
  --rule:#2C3036;--accent:#F0915A;--accent-ink:#F5A877;--accent-soft:#2A1E17;--accent-line:#4A2E1F;
  --cover-bg:#0B0C0E;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.25);
}
*{box-sizing:border-box}
html{font-family:"Inter",system-ui,-apple-system,sans-serif;font-size:17px;line-height:1.6;
  color:var(--ink);background:var(--paper);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper)}
.wrap{max-width:52rem;margin:0 auto;padding:0 16px}
a{color:var(--accent-ink)}
.mono{font-family:"JetBrains Mono",ui-monospace,monospace}
.kicker{font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0 0 .6rem}
header{padding:3.5rem 0 2.25rem;border-bottom:1px solid var(--rule)}
h1{font-size:clamp(2.1rem,7vw,3.2rem);line-height:1.04;letter-spacing:-.025em;font-weight:900;margin:0 0 1rem}
h1 span{color:var(--accent)}
.lead{font-size:1.08rem;color:var(--ink-soft);max-width:38rem;margin:0 0 1.5rem}
.stats{display:flex;flex-wrap:wrap;gap:.4rem 1.6rem;margin:0;padding:0;list-style:none;font-size:.85rem;color:var(--muted)}
.stats b{color:var(--ink);font-weight:700;font-size:1.05rem;margin-right:.25rem}
main{padding:2rem 0 1rem}
.book{display:grid;grid-template-columns:150px 1fr;gap:1.5rem;padding:1.75rem 0;border-bottom:1px solid var(--rule)}
.book:last-child{border-bottom:0}
.cover{display:block;aspect-ratio:108/192;background:var(--cover-bg);border-radius:6px;overflow:hidden;
  box-shadow:var(--shadow);transition:transform .15s ease}
.cover:hover{transform:translateY(-2px)}
.cover img{width:100%;height:100%;object-fit:contain;display:block}
.cover .sem-capa{display:flex;align-items:flex-end;height:100%;padding:12px;color:#F2EFE9;font-weight:800;line-height:1.1;font-size:1rem}
.info{min-width:0}
.info .kicker{color:var(--muted);letter-spacing:.1em}
h2{font-size:1.55rem;line-height:1.15;letter-spacing:-.015em;font-weight:800;margin:0 0 .45rem}
h2 a{color:var(--ink);text-decoration:none}
h2 a:hover{color:var(--accent-ink)}
.sub{color:var(--ink-soft);margin:0 0 .75rem}
.para{font-size:.9rem;color:var(--muted);margin:0 0 .85rem}
.para b{color:var(--ink-soft);font-weight:600}
.nums{display:flex;flex-wrap:wrap;gap:.35rem;margin:0 0 .85rem;padding:0;list-style:none}
.nums li{font-size:.76rem;padding:.18rem .55rem;border:1px solid var(--accent-line);background:var(--accent-soft);
  color:var(--accent-ink);border-radius:999px;font-weight:500}
.org{font-size:.85rem;color:var(--muted);margin:0 0 1rem}
.org b{color:var(--ink);font-weight:600}
.actions{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 .8rem}
.btn{display:inline-flex;align-items:center;gap:.4rem;font-size:.86rem;font-weight:600;text-decoration:none;
  padding:.5rem .9rem;border-radius:7px;border:1px solid var(--rule);color:var(--ink);background:var(--card);min-height:40px}
.btn:hover{border-color:var(--accent-line);color:var(--accent-ink)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{filter:brightness(1.07);color:#fff}
:root[data-theme="dark"] .btn.primary{color:#17191C}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .btn.primary{color:#17191C}}
.extra{font-size:.82rem;color:var(--muted);margin:0}
.extra a{white-space:nowrap}
footer{border-top:1px solid var(--rule);padding:1.75rem 0 3.5rem;font-size:.85rem;color:var(--muted)}
footer p{margin:0 0 .6rem}
@media (max-width:560px){
  header{padding-top:2.5rem}
  .book{grid-template-columns:96px 1fr;gap:1rem}
  h2{font-size:1.25rem}
  .sub{font-size:.95rem}
}
"""

ICONE_LER = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2z"/><path d="M22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/></svg>'
ICONE_PDF = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>'
ICONE_GIT = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="8" r="2.5"/><path d="M6 8.5v7"/><path d="M18 10.5c0 4-6 3-10.5 6"/></svg>'


def card(dados: dict, eb: dict) -> str:
    e = escape
    site = e(eb["site"])
    if eb.get("capa"):
        capa = f'<img src="{e(eb["capa"])}" alt="Capa de {e(eb["titulo"])}" width="420" height="747" loading="lazy">'
    else:
        capa = f'<span class="sem-capa">{e(eb["titulo"])}</span>'
    nums = "".join(f"<li>{e(n)}</li>" for n in eb["numeros"])
    org = f'Organizado por <b>{e(dados["autor"])}</b> e <b>{e(juntar(eb["coautoria_ia"]))}</b>'
    extras = []
    if eb.get("relacionados"):
        links = " · ".join(
            f'<a href="{e(url_repo(dados, r["repo"]))}">{e(r["nome"])}</a>' for r in eb["relacionados"])
        extras.append(f"Código: {links}")
    if eb.get("contexto"):
        extras.append(e(eb["contexto"]))
    if eb.get("licenca"):
        extras.append(e(eb["licenca"]))
    extra = "".join(f'<p class="extra">{x}</p>' for x in extras)
    para = f'<p class="para"><b>Para quem:</b> {e(eb["publico"])}</p>' if eb.get("publico") else ""
    return f"""
  <article class="book" id="{e(eb['slug'])}">
    <a class="cover" href="{site}" tabindex="-1" aria-hidden="true">{capa}</a>
    <div class="info">
      <p class="kicker">{e(eb['tipo'])} · v{e(eb['versao'])} · {e(mes_ano(eb['publicado_em']))}</p>
      <h2><a href="{site}">{e(eb['titulo'])}</a></h2>
      <p class="sub">{e(eb['subtitulo'])}</p>
      {para}
      <ul class="nums">{nums}</ul>
      <p class="org">{org}</p>
      <div class="actions">
        <a class="btn primary" href="{site}">{ICONE_LER}Ler online</a>
        <a class="btn" href="{e(url_pdf(dados, eb))}">{ICONE_PDF}PDF</a>
        <a class="btn" href="{e(url_repo(dados, eb['repo']))}">{ICONE_GIT}Repositório</a>
      </div>
      {extra}
    </div>
  </article>"""


def gerar_html(dados: dict) -> str:
    ebs = dados["ebooks"]
    paginas = sum(int(eb["paginas"]) for eb in ebs)
    ias = sorted({m.split()[0] for eb in ebs for m in eb["coautoria_ia"]})
    desde = min(eb["publicado_em"][:4] for eb in ebs) if ebs else ""
    cards = "".join(card(dados, eb) for eb in ebs)
    descricao = (f"{len(ebs)} ebooks técnicos abertos do {dados['autor']} ({dados['instituicao']}), "
                 "escritos em parceria com IA. Leitura no navegador ou em PDF para celular.")
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ebooks Abertos · Rogério Silva</title>
<meta name="description" content="{escape(descricao)}">
<meta property="og:title" content="Ebooks Abertos · {escape(dados['autor'])}">
<meta property="og:description" content="{escape(descricao)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{escape(dados['site'])}">
<meta name="theme-color" content="#17191C">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2317191C'/%3E%3Cpath d='M8 9h7a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H8zM24 9h-5' stroke='%23F0915A' stroke-width='2.6' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<!-- GERADO POR gerar.py A PARTIR DE catalogo.json. NÃO EDITE À MÃO. -->
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header>
  <p class="kicker">Biblioteca aberta · {escape(dados['instituicao'])}</p>
  <h1>Ebooks do Prof.<br><span>Rogério Silva</span></h1>
  <p class="lead">Manuais técnicos sobre desenvolvimento de software, escritos em parceria com IA e testados em sala de aula. Todos livres para ler, copiar e adaptar, no navegador ou em PDF no formato de tela de celular.</p>
  <ul class="stats">
    <li><b>{len(ebs)}</b>{'ebook' if len(ebs) == 1 else 'ebooks'}</li>
    <li><b>{paginas}</b>páginas</li>
    <li><b>{escape(' + '.join(ias))}</b>como coautor{'es' if len(ias) > 1 else ''}</li>
    <li><b>{escape(desde)}</b>primeira edição</li>
  </ul>
</header>
<main>{cards}
</main>
<footer>
  <p>Cada livro mora no seu próprio repositório, com a sua licença. Este índice é gerado a partir de <a href="https://github.com/{escape(dados['github'])}/{escape(dados['github'])}.github.io/blob/main/catalogo.json" class="mono">catalogo.json</a>; para incluir um livro novo, veja o <a href="https://github.com/{escape(dados['github'])}/{escape(dados['github'])}.github.io/blob/main/AGENTS.md" class="mono">AGENTS.md</a>.</p>
  <p>{escape(dados['autor'])} · <a href="https://github.com/{escape(dados['github'])}">github.com/{escape(dados['github'])}</a></p>
</footer>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------- README

def gerar_readme(dados: dict) -> str:
    ebs = dados["ebooks"]
    linhas = []
    for eb in ebs:
        links = (f"[ler online]({eb['site']}) · [PDF]({url_pdf(dados, eb)}) · "
                 f"[repositório]({url_repo(dados, eb['repo'])})")
        if eb.get("relacionados"):
            links += " · " + " · ".join(
                f"[{r['nome']}]({url_repo(dados, r['repo'])})" for r in eb["relacionados"])
        linhas.append(
            f"### [{eb['titulo']}]({eb['site']})\n\n"
            f"{eb['subtitulo']}\n\n"
            f"{eb['tipo']} v{eb['versao']} · {mes_ano(eb['publicado_em'])} · "
            f"organizado por {dados['autor']} e {juntar(eb['coautoria_ia'])}  \n"
            f"{' · '.join(eb['numeros'])}\n\n"
            f"{links}\n")
    paginas = sum(int(eb["paginas"]) for eb in ebs)
    return f"""<!-- GERADO POR gerar.py A PARTIR DE catalogo.json. NÃO EDITE À MÃO. -->
# Ebooks do Prof. Rogério Silva

Índice dos ebooks técnicos abertos do {dados['autor']} ({dados['instituicao']}), escritos em parceria com IA. **{len(ebs)} livros · {paginas} páginas.**

**Site:** {dados['site']}

## Livros

{chr(10).join(linhas)}
## Como este índice funciona

| Arquivo | Papel |
|---|---|
| `catalogo.json` | fonte única de verdade: um registro por livro |
| `gerar.py` | gera `index.html` e `README.md` a partir do catálogo (só biblioteca padrão) |
| `capas/` | capa de cada livro em WebP, tirada da página 1 do PDF |
| `AGENTS.md` | o roteiro que qualquer agente (Claude, Gemini, Codex) segue para registrar um livro novo |
| `.github/workflows/indice.yml` | regenera o site a cada push, inclusive quando o catálogo é editado pela web |

Para incluir um livro: adicione o registro em `catalogo.json`, a capa em `capas/`, rode `python gerar.py` e faça o commit. O passo a passo completo está em [`AGENTS.md`](AGENTS.md).

## Licença

Cada livro tem a licença declarada no próprio repositório. Este índice: texto CC BY-SA 4.0, `gerar.py` MIT.
"""


def main() -> None:
    dados = carregar()
    saidas = {RAIZ / "index.html": gerar_html(dados), RAIZ / "README.md": gerar_readme(dados)}
    if "--verificar" in sys.argv:
        velhos = [p.name for p, txt in saidas.items()
                  if not p.exists() or p.read_text(encoding="utf-8") != txt]
        if velhos:
            sys.exit(f"Desatualizado: {', '.join(velhos)}. Rode: python gerar.py")
        print("Índice em dia.")
        return
    for p, txt in saidas.items():
        p.write_text(txt, encoding="utf-8")
    print(f"{len(dados['ebooks'])} ebooks → index.html, README.md")


if __name__ == "__main__":
    main()
