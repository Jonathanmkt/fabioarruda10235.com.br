# fabioarruda

Site de **Fábio Arruda** — pré-candidato a Deputado Estadual por São Paulo (Republicanos).
Domínio definido: **`fabioarruda10235.com.br`**, contratação em andamento no Registro.br
(informado pelo CEO em 15/08/2026). A pasta local se chama `fabioarruda` — pode ser renomeada
quando o registro sair. `CNAME` já está no repositório, pronto para quando o DevOps configurar o
Cloudflare — mesmo fluxo usado no `bombeiroflaviosantos.com.br`.

Hoje no ar apenas a **página de espera** (uma tela, sem navegação), V1 inicial, enquanto o site
definitivo é construído. Commit inicial feito e remote configurado
(`github.com/Jonathanmkt/fabioarruda10235.com.br`) em 15/08/2026 — falta só o push (exclusivo do
CEO) e o apontamento de DNS no Cloudflare.

## Arquivos

```
index.html         a página inteira: HTML, CSS e conteúdo, sem dependência externa
assets/fabio.jpg    retrato do candidato
CNAME               o domínio, exigido pelo GitHub Pages — pronto para o deploy futuro
```

## De onde veio cada informação da página

| Afirmação | Fonte |
|---|---|
| Pré-candidato a Deputado Estadual por São Paulo, Republicanos | Bio do Instagram `@fabioarrudasaopaulo` |
| "Trabalho, experiência e compromisso com São Paulo" | Frase do próprio candidato, no Instagram |
| Pedágio zero para caminhão que transporta alimentos | Bio do Instagram `@fabioarrudasaopaulo` |
| Retrato | Foto de perfil pública do Instagram `@fabioarrudasaopaulo`, 150×150 px |
| Número 10235 | Domínio de campanha `fabioarruda10235.com.br`, informado pelo CEO em 15/08/2026 |

## ⚠️ Pendências conhecidas

1. **A pauta está incompleta** — só a bandeira do pedágio zero apareceu na bio do Instagram até
   agora. Ampliar quando vier mais material de campanha.
2. **O número 10235 veio do domínio de campanha, não de fonte eleitoral oficial.** Vale reconferir
   no TSE quando possível — o Instagram sozinho mencionava só "10", que é o número nacional do
   Republicanos.
3. **O retrato está em 150×150 px**, capturado do perfil público do Instagram. Ao receber a foto
   oficial, basta substituir `assets/fabio.jpg`.
4. **Domínio `fabioarruda10235.com.br` confirmado pelo CEO, mas ainda em contratação** no
   Registro.br.
5. Commit inicial feito e remote configurado em 15/08/2026 — falta o push (exclusivo do CEO) e o
   apontamento de DNS. DNS/Cloudflare entram quando o CEO acionar o `devops-infra`.
