# fabioarruda

Site de **Fábio Arruda** — candidato a Deputado Estadual por São Paulo (Republicanos), nº 10235.
Domínio: **`fabioarruda10235.com.br`**, registrado, com DNS apontado e certificado ativo desde
15/08/2026 (DevOps).

**No ar**, publicado — uma tela, sem navegação, com hierarquia de peça de campanha.

## A hierarquia da página, e por quê

A ordem de leitura foi montada para o que o eleitor precisa reter, não para o que a página tem
a dizer:

1. **`Deputado Estadual`** — o cargo pretendido é o título de maior peso, por decisão do CEO
   (15/08/2026). Projeta a pessoa no cargo; "candidato" é palavra fraca e não entra como título.
2. **O nome** — o ativo de marca, em Montserrat Black.
3. **O número de urna (10235)** — em bloco sólido, porque é o que se digita na urna.
4. **O slogan** — a frase do próprio candidato.
5. **A bandeira** — uma proposta concreta vale mais que três genéricas.
6. **Compartilhar** — em campanha brasileira o site não é destino, é peça que circula no
   WhatsApp; o botão usa `navigator.share` no celular e cai no `wa.me` onde não houver.

## Arquivos

```
index.html            a página: HTML, CSS e conteúdo, sem nenhuma requisição externa
assets/fabio.jpg      retrato do candidato
assets/og.jpg         1200×630 — o card que WhatsApp e Facebook exibem ao compartilhar o link
assets/fontes.css     Montserrat (3 pesos) embutida em base64, licença SIL OFL
scripts/gera-og.py    refaz o assets/og.jpg — mude o CFG no fim do arquivo e rode
scripts/gera-fontes.py refaz o assets/fontes.css a partir da Montserrat instalada na máquina
CNAME                 o domínio, exigido pelo GitHub Pages
```

**A fonte é embutida de propósito.** Montserrat existe nesta máquina, não na do eleitor — site que
depende de fonte instalada quebra silenciosamente para quem visita. Os 3 pesos subsetados aos
caracteres do português custam 41 KB e não fazem nenhuma requisição externa.

## Peso e verificação

| | |
|---|---|
| **Primeira visita** | 55 KB no total (HTML 11 KB + fontes 41 KB + retrato 4 KB) |
| **Requisições externas** | nenhuma |
| **Console** | sem erro; nenhuma requisição quebrada |
| **Larguras conferidas** | 360 px, 375 px e 1280 px — sem transbordo horizontal |
| **Contraste** | todos os textos passam em WCAG AA, medido no pior fundo da página |
| **Teclado** | foco visível (3 px, `:focus-visible`), ordem de tabulação conferida |
| **SEO** | `title`, description, canônico, Open Graph, Twitter card e JSON-LD `Person` |

## De onde veio cada informação da página

| Afirmação | Fonte |
|---|---|
| Candidato a Deputado Estadual por São Paulo, Republicanos | Bio do Instagram `@fabioarrudasaopaulo`; status "candidato" (não mais pré) confirmado pelo CEO em 15/08/2026 |
| "Trabalho, experiência e compromisso com São Paulo" | Frase do próprio candidato, no Instagram |
| Pedágio zero para caminhão que transporta alimentos | Bio do Instagram `@fabioarrudasaopaulo` |
| Retrato | Foto de perfil pública do Instagram `@fabioarrudasaopaulo`, 150×150 px |
| Número 10235 | Domínio de campanha `fabioarruda10235.com.br`, informado pelo CEO em 15/08/2026 |
| Texto de apoio da bandeira ("o pedágio que o caminhão paga chega na conta do supermercado") | **Escrito aqui**, em 15/08/2026, a pedido do CEO. Não veio do candidato nem da Comunicação — trocar quando vier a copy oficial |

## ⚠️ Pendências conhecidas

1. **A pauta está incompleta** — só a bandeira do pedágio zero apareceu na bio do Instagram até
   agora. Ampliar quando vier mais material de campanha.
2. **O número 10235 veio do domínio de campanha, não de fonte eleitoral oficial.** Vale reconferir
   no TSE quando possível — o Instagram sozinho mencionava só "10", que é o número nacional do
   Republicanos.
3. **O retrato está em 150×150 px**, capturado do perfil público do Instagram. Ao receber a foto
   oficial, basta substituir `assets/fabio.jpg`.
4. `robots` mudou de `noindex, nofollow` para `index, follow` em 15/08/2026, quando o site saiu do
   ar só interno e passou a ser publicado de verdade.
5. **A página não usa o imperativo "vote".** O número aparece como informação ("Urna 10235"), não
   como pedido de voto, porque a propaganda eleitoral tem janela legal própria. Quem confirma o que
   pode ser dito, e a partir de quando, é o `assessor-juridico` — não foi consultado nesta rodada.
6. **O retrato de 150×150 px limita o card de compartilhamento.** O `og.jpg` amplia essa origem
   para 300 px com Lanczos e realce; funciona no tamanho em que o WhatsApp exibe, mas a foto
   oficial em alta resolução melhoraria visivelmente. Ao trocar `assets/fabio.jpg`, rode
   `python scripts/gera-og.py` para refazer o card.
