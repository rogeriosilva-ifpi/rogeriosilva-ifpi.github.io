<!-- GERADO POR gerar.py A PARTIR DE catalogo.json. NÃO EDITE À MÃO. -->
# Ebooks do Prof. Rogério Silva

Índice dos ebooks técnicos abertos do Prof. Rogério Silva (IFPI · Instituto Federal do Piauí), escritos em parceria com IA. **4 livros · 814 páginas.**

**Site:** https://rogeriosilva-ifpi.github.io/

## Livros

### [Desenvolvimento Dirigido por IA](https://rogeriosilva-ifpi.github.io/ia-dev-ebook/)

Manual de campo para desenvolver no dia a dia com agentes de código como Claude Code, OpenAI Codex e Antigravity CLI.

Manual de campo v1.0 · setembro de 2026 · organizado por Prof. Rogério Silva e Claude Opus 5  
28 capítulos · 127 páginas · 16 diagramas

[ler online](https://rogeriosilva-ifpi.github.io/ia-dev-ebook/) · [PDF](https://github.com/rogeriosilva-ifpi/ia-dev-ebook/raw/main/Desenvolvimento-Dirigido-por-IA.pdf) · [EPUB](https://github.com/rogeriosilva-ifpi/ia-dev-ebook/raw/main/Desenvolvimento-Dirigido-por-IA.epub) · [repositório](https://github.com/rogeriosilva-ifpi/ia-dev-ebook)

### [Arquitetura em Tempos de IA](https://rogeriosilva-ifpi.github.io/arquitetura-ia-ebook/)

Repensando Clean Architecture, DDD e SOLID para agentes autônomos.

Ensaio técnico v1.0 · outubro de 2026 · organizado por Prof. Rogério Silva e Claude Opus 5  
5 capítulos + introdução e epílogo · 220 páginas · 12 diagramas · 6 instrumentos

[ler online](https://rogeriosilva-ifpi.github.io/arquitetura-ia-ebook/) · [PDF](https://github.com/rogeriosilva-ifpi/arquitetura-ia-ebook/raw/main/Arquitetura-em-Tempos-de-IA.pdf) · [EPUB](https://github.com/rogeriosilva-ifpi/arquitetura-ia-ebook/raw/main/Arquitetura-em-Tempos-de-IA.epub) · [repositório](https://github.com/rogeriosilva-ifpi/arquitetura-ia-ebook)

### [Crachá & Porta](https://rogeriosilva-ifpi.github.io/cracha-e-porta-ebook/)

Autenticação e autorização em backends Express e FastAPI, do zero até o nível de um sênior, inclusive quando é a IA que escreve o código.

Manual de campo v1.0 · outubro de 2026 · organizado por Prof. Rogério Silva e Claude Opus 5.5  
16 capítulos · 223 páginas · 54 ataques reproduzíveis · 8 instrumentos

[ler online](https://rogeriosilva-ifpi.github.io/cracha-e-porta-ebook/) · [PDF](https://github.com/rogeriosilva-ifpi/cracha-e-porta-ebook/raw/main/Cracha-e-Porta.pdf) · [EPUB](https://github.com/rogeriosilva-ifpi/cracha-e-porta-ebook/raw/main/Cracha-e-Porta.epub) · [repositório](https://github.com/rogeriosilva-ifpi/cracha-e-porta-ebook) · [Laboratório Express 5 + TypeScript](https://github.com/rogeriosilva-ifpi/cracha-e-porta-express) · [Laboratório FastAPI + Python](https://github.com/rogeriosilva-ifpi/cracha-e-porta-fastapi)

### [Estado & Tela](https://rogeriosilva-ifpi.github.io/estado-e-tela-ebook/)

Aplicações web reativas com React, do DOM manipulado à mão até uma aplicação completa, autenticada e testada, construída com agentes de IA sem perder o controle do código.

Manual de campo v1.0 · novembro de 2026 · organizado por Prof. Rogério Silva e Claude Opus 5.5  
20 capítulos · 244 páginas · 22 figuras · 21 ilustrações

[ler online](https://rogeriosilva-ifpi.github.io/estado-e-tela-ebook/) · [PDF](https://github.com/rogeriosilva-ifpi/estado-e-tela-ebook/raw/main/Estado-e-Tela.pdf) · [EPUB](https://github.com/rogeriosilva-ifpi/estado-e-tela-ebook/raw/main/Estado-e-Tela.epub) · [repositório](https://github.com/rogeriosilva-ifpi/estado-e-tela-ebook)

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
