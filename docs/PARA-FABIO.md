# History Tube — Guia para o Fabio 🎬

Bem-vindo ao motor que leva um episódio do **History Tube** da ideia até o vídeo
empacotado. Este guia explica, em português e sem juridiquês, **como a coisa funciona**
e **o que você faz** no dia a dia.

> A regra de ouro: **os agentes propõem; você decide.** A criatividade — o ângulo, os
> cortes de câmera, a luz e o empacotamento (título/thumbnail) — é **sua**. O sistema
> existe para tirar o trabalho braçal do caminho e te deixar decidir mais, não menos.

---

## 1. A ideia em uma frase

Um episódio passa por **9 fases** e para em **5 portões (gates)** onde você aprova
antes de gastar tempo/créditos. O David Hattenborg aparece **só na abertura e no
fecho** (os "bookends"); o corpo do vídeo é b-roll histórico gerado por IA.

---

## 2. A equipe (a "crew" do David)

Cada agente é um especialista. Os nomes são apelidos — a função é o que importa:

| Apelido | Função | O que entrega |
|---|---|---|
| **Vitória** | Showrunner (a chefe / orquestradora) | Conduz tudo, chama o agente certo, **para nos portões** |
| **Deborah** | Pesquisadora | Dossiê + fontes + proposta de título/thumbnail |
| **Katusha** | Conceito | O arco dramático (batidas, o clímax, "o que vem depois") |
| **Tainara** | Crítica | Ataca o roteiro: precisão, clímax, riscos (temas sensíveis) |
| **Glesy** | Roteirista | O roteiro completo, na voz teatral do David |
| **Brenda** | Direção | Rascunho da lista de planos (câmera + luz propostas) |
| **Sabrina** | Prompts | Converte cada plano em prompts prontos pro Higgsfield |
| **Wanessa** | Render | Gera clipes + voz (TTS) e puxa a música do Suno |
| **Cleidiane** | Edição | Monta o corte: vídeo + voz + música abafada + legendas |
| **Jucilene** | Shorts | Tira 1–2 Shorts verticais (9:16) do vídeo pronto |

A Vitória **nunca publica sozinha** — o passo final (publicar) é sempre seu.

---

## 3. O fluxo: 9 fases, 5 portões

```
Ideia → [Deborah] → 🚦 GATE 1 (você aprova título + ângulo + thumbnail)
      → [Katusha + Tainara] → roteiro tem que fechar
      → [Glesy] → 🚦 GATE 2 (você trava o roteiro)
      → [Brenda] → 🚦 GATE 3 (VOCÊ ajusta câmera + luz, plano a plano — seu domínio)
      → [Sabrina] → prompts
      → [Wanessa] → 🔎 REVISÃO LEVE (você escolhe o melhor take)
      → [Cleidiane] → 🚦 GATE 4 (você assiste o corte e confirma o empacotamento)
      → Agendado → VOCÊ publica → [Jucilene] gera os Shorts
```

**Por que os portões existem:** o Gate 1 te protege de gastar créditos numa ideia
fraca; o Gate 2 congela a base; o Gate 3 é a sua direção criativa (a única coisa que o
sistema nunca decide por você); o Gate 4 garante que nada vai pro ar sem você ver.

---

## 4. Como rodar (linha de comando)

No terminal, dentro da pasta do projeto:

```bash
python cli.py demo               # roda um episódio de exemplo do começo ao fim (modo teste)
python cli.py crew               # mostra a equipe

python cli.py init roma --title "A Queda de Roma" --angle "Não foi um colapso, foi um esquecimento"
python cli.py run roma           # avança e PARA no próximo portão, te mostrando o que aprovar
python cli.py approve roma       # você aprova o portão pendente → continua
python cli.py status roma        # em que fase está o episódio?
python cli.py publish roma       # publica (só você faz isso)
```

- `run` para em cada portão e espera você. `approve` libera.
- `run roma --auto` aprova **tudo** automaticamente — útil só pra teste, não pra valer.
- Tudo que cada agente produz fica em `episodes/<slug>/` (dossiê, roteiro, lista de
  planos, prompts, legendas, plano de edição, Shorts).

---

## 5. Modo "teste" vs "pra valer"

O sistema já roda **do início ao fim em modo de teste (mock)** — sem chave, sem
internet, sem FFmpeg. Ele cria arquivos de exemplo (placeholders) pra você ver o
formato. Para gerar **vídeo de verdade**, você liga os serviços reais com variáveis de
ambiente:

| Variável | Teste (padrão) | Pra valer |
|---|---|---|
| `HT_LLM` | `mock` | `anthropic` (escreve com o Claude de verdade) |
| `HT_HIGGSFIELD` | `mock` | `api` (gera clipes + voz no Higgsfield) |
| `HT_STORE` | `local` | `notion` (estado no seu Notion) |

Enquanto não estiver configurado, o adaptador real **avisa na cara** (não falha
silenciosamente).

---

## 6. O que você precisa fazer pra começar (uma vez só)

1. **Instalar** no Windows: Python, Git, **FFmpeg** e **Whisper** (confirme que `ffmpeg`
   e `whisper` rodam no terminal).
2. **Clonar** o repositório e rodar `python cli.py demo` pra ver funcionando.
3. **Conectar os MCPs** no seu Claude: **Higgsfield** (sua conta) e **Notion**.
   O Suno é manual (você gera a música no site e joga em `episodes/<slug>/audio/music/`).
4. **Criar o Notion** a partir de [`docs/notion-schema-spec.md`](notion-schema-spec.md).
5. **Travar a identidade do David** (as duas coisas que só você decide):
   - a **voz** em `config/voice-recipe.json` (a "receita" da voz, pra ser portável);
   - as **referências visuais** em `config/visual-refs/` (David + a Bússola Chronos).

Passo a passo completo: [`docs/fabio-setup-checklist.md`](fabio-setup-checklist.md).

---

## 7. Regras que não mudam

- **Roda no Windows.** Nada de coisa só-de-Mac. Tudo é Python + FFmpeg + Whisper.
- **Voz e música são faixas separadas** — a edição abafa a música embaixo da narração.
- **A alma do canal:** narração histórica que **constrói um arco até um clímax
  emocional**. Se um rascunho fugir disso, ele está errado — a alma manda.

---

## 8. Onde está cada coisa

- **A fonte da verdade** (o plano inteiro): [`docs/build-plan.md`](build-plan.md).
- **A constituição criativa** (lida por todo agente): [`config/channel-dna.md`](../config/channel-dna.md).
- **Como o código funciona** (mais técnico): [`CLAUDE.md`](../CLAUDE.md).
- **Seu checklist de instalação:** [`docs/fabio-setup-checklist.md`](fabio-setup-checklist.md).

Qualquer dúvida, o JJ te dá um help. Bom filme. 🎥
