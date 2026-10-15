# AGENTS.md — índice de ebooks do Prof. Rogério Silva

Este repositório é a **raiz** de todos os ebooks abertos do Prof. Rogério Silva (IFPI). Ele não contém livros: contém o catálogo que aponta para eles e o site gerado em https://rogeriosilva-ifpi.github.io/.

Vale para qualquer agente de código (Claude Code, Gemini CLI, Codex, Antigravity CLI) e para humanos.

## Regras

1. **`catalogo.json` é a fonte única de verdade.** `index.html` e `README.md` são gerados por `gerar.py`. Nunca edite esses dois à mão: a próxima geração apaga a edição.
2. **Não invente números.** Capítulos, páginas, diagramas e instrumentos vêm do README do próprio livro (linha de métricas logo abaixo do título). Se o README do livro não diz, o catálogo também não diz.
3. **Coautoria com o nome exato do modelo**, como aparece na capa do livro: `"Claude Opus 5.5"`, `"Gemini 3 Pro"`. Um livro feito com mais de um modelo lista todos, na ordem de contribuição.
4. **Só entra livro publicado**: repositório público, PDF na raiz do repositório e GitHub Pages ativo.
5. `gerar.py` usa apenas a biblioteca padrão do Python. Mantenha assim.

## Registrar um livro novo

Pré-requisito: o livro já está no repositório próprio, com nome `<slug>-ebook` (padrão atual: `ia-dev-ebook`, `arquitetura-ia-ebook`, `cracha-e-porta-ebook`), PDF na raiz da branch `main` e Pages publicado em `https://rogeriosilva-ifpi.github.io/<repo>/`.

1. **Capa.** Gere a capa a partir da página 1 do PDF (precisa de `pdftoppm` e Pillow):

   ```bash
   pdftoppm -f 1 -l 1 -r 110 -png ../<repo>/<Arquivo>.pdf /tmp/capa
   python3 -c "from PIL import Image, ImageOps; im=Image.open('/tmp/capa-1.png').convert('RGB'); im=im.crop(ImageOps.invert(im).getbbox()); w=420; im.resize((w,int(im.size[1]*w/im.size[0])),Image.LANCZOS).save('capas/<repo>.webp','WEBP',quality=82)"
   ```

   (O sufixo do PNG pode ser `-1`, `-01` ou `-001`, conforme o número de páginas do PDF. O `crop` remove a margem branca que alguns PDFs têm em volta da capa.)

2. **Registro.** Acrescente um objeto em `ebooks` no `catalogo.json`. A ordem no arquivo não importa: o site ordena por `publicado_em`, do mais recente para o mais antigo.

   | Campo | Obrigatório | Exemplo |
   |---|---|---|
   | `slug` | sim | `"cracha-e-porta"` (único; vira a âncora `#slug` no site) |
   | `titulo` | sim | `"Crachá & Porta"` |
   | `subtitulo` | sim | uma frase, a mesma da capa ou do README do livro |
   | `tipo` | sim | `"Manual de campo"`, `"Ensaio técnico"` |
   | `versao` | sim | `"1.0"` |
   | `publicado_em` | sim | `"2026-10"` (AAAA-MM) |
   | `coautoria_ia` | sim | `["Claude Opus 5.5"]` |
   | `numeros` | sim | `["16 capítulos", "223 páginas"]`, copiado do README do livro |
   | `paginas` | sim | `223` (número; entra no total do site) |
   | `repo` | sim | `"cracha-e-porta-ebook"` |
   | `site` | sim | URL do GitHub Pages do livro, com `/` no fim |
   | `pdf` | sim | nome do arquivo na raiz do repo, ex. `"Cracha-e-Porta.pdf"` |
   | `publico` | não | uma frase: para quem é |
   | `capa` | não | `"capas/<repo>.webp"`; sem ela o site mostra uma capa tipográfica |
   | `temas` | não | lista de palavras-chave |
   | `contexto` | não | disciplina ou projeto de origem, ex. `"TEC.1052 Programação para Internet II · ADS · IFPI"` |
   | `relacionados` | não | `[{"nome": "Laboratório FastAPI + Python", "repo": "cracha-e-porta-fastapi"}]` |
   | `licenca` | não | `"Texto CC BY-SA 4.0 · código MIT"` |

3. **Gerar e conferir.**

   ```bash
   python3 gerar.py
   python3 gerar.py --verificar   # deve imprimir "Índice em dia."
   ```

   Abra `index.html` no navegador e confira o card novo (capa, links de site, PDF e repositório).

4. **Commit.** `git add catalogo.json capas/ index.html README.md && git commit -m "indice: adiciona <titulo>"` e push na `main`. O Pages publica em um ou dois minutos.

5. **Link de volta.** No README do livro novo, logo abaixo do título, acrescente:

   ```markdown
   Parte da [biblioteca de ebooks abertos do Prof. Rogério Silva](https://rogeriosilva-ifpi.github.io/).
   ```

## Atualizar um livro existente

Nova versão, novo número de páginas, nova capa: altere o registro no `catalogo.json` (e a capa em `capas/`, se mudou), rode `python3 gerar.py` e faça o commit. Não mude o `slug`: links externos apontam para `#slug`.

## Editar pela web, sem instalar nada

Edite `catalogo.json` direto no GitHub. O workflow `.github/workflows/indice.yml` roda `gerar.py` e faz o commit do `index.html` e do `README.md` atualizados. A capa, nesse caso, precisa ser enviada pelo botão *Add file → Upload files* na pasta `capas/`.
