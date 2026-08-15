# Histórico — site fabioarruda10235.com.br

Diário do projeto. Append-only, entrada mais recente no topo.

## 2026-08-15 — Reconstrução com olhar de marketing e comunicação política

**O quê:** A página de espera virou peça de campanha. Hierarquia refeita: "Deputado Estadual" (o
cargo pretendido, não "candidato") passou a ser o título de maior peso, acima do nome; o número de
urna 10235 ganhou bloco visual sólido. Tipografia Montserrat foi embutida em `assets/fontes.css`
(3 pesos, woff2 base64, licença SIL OFL) para não depender de fonte instalada na máquina do
visitante. Card de compartilhamento 1200×630 criado (`assets/og.jpg`) com cargo, nome, número e
slogan, e as meta tags Open Graph/Twitter passaram para `summary_large_image`. Novo botão
"Compartilhar" via `navigator.share`, com queda para `wa.me`. Contraste do rodapé, que reprovava
WCAG AA (3,89:1), corrigido subindo o alpha de .58 para .78. JSON-LD `Person` adicionado para SEO.
Dois scripts novos e versionados para regenerar os ativos: `scripts/gera-og.py` (Pillow) e
`scripts/gera-fontes.py` (fontTools).

**Por quê:** decisão explícita do CEO de projetar a pessoa no cargo pretendido — "candidato" é
palavra fraca para título. Em campanha brasileira o link circula sobretudo no WhatsApp, então o
card de compartilhamento é o que a maioria do eleitorado realmente vê antes de abrir o site; e a
fonte só existia na máquina de quem construiu o site, então o visitante caía no fallback sem que
ninguém percebesse. O texto de apoio da bandeira do pedágio zero foi escrito nesta rodada, a
pedido do CEO, na ausência de copy oficial do candidato ou da Comunicação — pendência registrada
no README para troca quando a copy chegar. A página evita o imperativo "vote" porque a janela
legal da propaganda eleitoral não foi confirmada com o `assessor-juridico` nesta rodada.

**Arquivos-chave:** `index.html`, `assets/fontes.css` (novo), `assets/og.jpg` (novo),
`scripts/gera-og.py` e `scripts/gera-fontes.py` (novos), `README.md`.
