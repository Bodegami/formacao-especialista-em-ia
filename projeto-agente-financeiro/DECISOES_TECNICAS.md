# Decisões técnicas

Registro das principais decisões técnicas do projeto. Cada uma traz o contexto, a
decisão tomada, o motivo e as alternativas que foram descartadas.

[← Voltar ao README](README.md)

---

## Sumário

| ID | Decisão |
|---|---|
| [DT-01](#dt-01--o-llm-interpreta-o-código-decide) | O LLM interpreta, o código decide |
| [DT-02](#dt-02--clean-architecture-em-camadas) | Clean Architecture em camadas |
| [DT-03](#dt-03--decimal-em-vez-de-float) | `Decimal` em vez de `float` |
| [DT-04](#dt-04--conversão-estrita-de-valores) | Conversão estrita de valores, sem adivinhar |
| [DT-05](#dt-05--valor-recebido-como-texto-pelas-ferramentas) | Valor recebido como texto pelas ferramentas |
| [DT-06](#dt-06--ferramentas-retornam-okerro-com-valores-já-formatados) | Ferramentas retornam `OK:`/`ERRO:` com valores já formatados |
| [DT-07](#dt-07--langchain-create_agent) | LangChain `create_agent` |
| [DT-08](#dt-08--gemini-38-flash-com-temperatura-0) | Gemini 3.8 Flash com temperatura 0 |
| [DT-09](#dt-09--system-prompt-como-segunda-linha-de-defesa) | System prompt como segunda linha de defesa |
| [DT-10](#dt-10--guardas-determinísticas-antes-do-llm) | Guardas determinísticas antes do LLM |
| [DT-11](#dt-11--turnguard-contra-chamadas-duplicadas) | `TurnGuard` contra chamadas duplicadas |
| [DT-12](#dt-12--lock-nas-ferramentas) | Lock nas ferramentas |
| [DT-13](#dt-13--limite-de-recursão-e-tratamento-de-falhas) | Limite de recursão e tratamento de falhas |
| [DT-14](#dt-14--estado-em-memória-por-sessão) | Estado em memória, por sessão |
| [DT-15](#dt-15--streamlit-com-tema-próprio) | Streamlit com tema próprio |
| [DT-16](#dt-16--recibos-gerados-a-partir-da-transação-real) | Recibos gerados a partir da transação real |
| [DT-17](#dt-17--tdd-e-duas-camadas-de-teste) | TDD e duas camadas de teste |
| [DT-18](#dt-18--uv-para-ambiente-e-dependências) | `uv` para ambiente e dependências |
| [DT-19](#dt-19--chave-de-api-fora-do-código) | Chave de API fora do código |

---

## DT-01 — O LLM interpreta, o código decide

- **Contexto:** o enunciado exige zero erros de cálculo e validações dentro das
  ferramentas, não apenas no prompt.
- **Decisão:** o modelo só traduz linguagem natural em chamadas de ferramenta.
  Validação, cálculo, alteração de saldo e formatação ficam no código.
- **Por quê:** um LLM pode errar contas ou ser manipulado por jailbreak. Se a
  regra vive no código, ela vale mesmo quando o modelo "desobedece". O pior que um
  modelo manipulado consegue fazer é chamar uma das três ferramentas, e elas recusam
  entradas inválidas.
- **Alternativa descartada:** deixar o modelo calcular o novo saldo e só "conferir"
  no código. Isso duplicaria a lógica e abriria espaço para divergência.

## DT-02 — Clean Architecture em camadas

- **Decisão:** separar o projeto em quatro camadas:
  - `domain`: `Account`, `money`, erros
  - `application`: casos de uso e porta `AccountRepository`
  - `infrastructure`: repositório em memória
  - `agent` e `ui`: adaptadores para LangChain e Streamlit
- **Por quê:** o domínio não importa nada de LangChain, Gemini ou Streamlit. As
  regras de negócio são testadas em milissegundos, sem rede e sem LLM. Trocar o
  modelo, o framework de agente ou a interface não toca nas regras.
- **Detalhes:**
  - Um caso de uso por operação (`GetBalanceUseCase`, `DepositUseCase`,
    `TransferUseCase`), em vez de um "serviço" genérico.
  - Os casos de uso retornam DTOs imutáveis, para que a entidade não vaze para fora.
- **Alternativa descartada:** um único arquivo com tudo. É mais curto, mas mistura
  regra de negócio com detalhes do framework e dificulta os testes.

## DT-03 — `Decimal` em vez de `float`

- **Decisão:** todo valor monetário é `Decimal` com exatamente 2 casas (`quantize`).
- **Por quê:** `float` tem erro de representação binária (`0.1 + 0.2 =
  0.30000000000000004`). Em dinheiro isso é inaceitável. Com `Decimal`, a sequência
  `+0,10 +0,20 −0,30` resulta exatamente em zero, e há um teste para isso.
- **Alternativa descartada:** inteiros em centavos. Também é exato, mas exige
  converter em toda entrada e saída e deixa o código menos legível.

## DT-04 — Conversão estrita de valores

- **Decisão:**
  - Aceitar só formatos sem ambiguidade (`250`, `250.50`, `250,50`).
  - Recusar valores com possível separador de milhar (`1.000`, `10,555`).
  - Recusar mais de 2 casas decimais, em vez de arredondar.
  - Limitar a 13 dígitos inteiros.
- **Por quê:** o enunciado diz "nunca arredondar errado" e "não executar operações
  ambíguas". `1.000` é mil no Brasil e um nos EUA. Adivinhar pode gerar um erro de
  mil vezes. Recusar e pedir o valor de novo é seguro.
- **Detalhe:** o limite de 13 dígitos evita que um número gigante estoure a precisão
  do `Decimal`, que geraria uma exceção não tratada.

## DT-05 — Valor recebido como texto pelas ferramentas

- **Decisão:** o parâmetro `valor` das ferramentas é `str`. A descrição da
  ferramenta pede ao modelo que repasse o número **exatamente como o usuário
  escreveu**, sem converter.
- **Por quê:** a conversão e a validação ficam no código (DT-04), não no modelo.
  Também evita que o modelo transforme "1.000" em `1.0` ou `1000` por conta própria.

## DT-06 — Ferramentas retornam `OK:`/`ERRO:` com valores já formatados

- **Decisão:**
  - Toda ferramenta devolve uma frase pronta, começando com `OK:` ou `ERRO:`, com
    os valores já em `R$ 1.250,00`.
  - Exceções de domínio viram `ERRO: <motivo>. Nenhum valor foi alterado.`
  - Exceções inesperadas viram uma mensagem genérica, sem stack trace.
- **Por quê:** o modelo só repassa a informação e não precisa refazer contas nem
  formatar. O prefixo também deixa claro para o modelo, e para a interface, se a
  operação aconteceu.

## DT-07 — LangChain `create_agent`

- **Decisão:** usar `langchain.agents.create_agent` (LangChain 1.x, sobre LangGraph),
  com as três ferramentas e o system prompt.
- **Por quê:** é a API atual do LangChain para agentes com function calling. Ela
  executa o loop modelo ↔ ferramentas e aceita qualquer chat model. Trocar o Gemini
  por outro provedor exige mudar só a função `create_gemini_model`.
- **Detalhe:** o grafo é criado sob demanda (lazy), na primeira mensagem que chega
  ao LLM. Assim, as guardas de entrada (DT-10) podem ser testadas sem modelo nenhum.

## DT-08 — Gemini 3.8 Flash com temperatura 0

- **Decisão:** usar o modelo `gemini-3.8-flash` com `temperature=0` e
  `max_retries=2`, configurável pela variável `GEMINI_MODEL`.
- **Por quê:**
  - Temperatura 0 deixa o comportamento o mais previsível possível.
  - O modelo "flash" é rápido, e uma resposta lenta quebra a sensação de conversa.
  - O `gemini-2.5-flash` não está mais disponível para contas novas; a própria API
    recomenda o 3.8.

## DT-09 — System prompt como segunda linha de defesa

- **Decisão:** o prompt é organizado em seções: papel, operações permitidas, escopo,
  confiabilidade, ambiguidade, segurança e estilo. A recusa usa uma **mensagem fixa**.
- **Por quê:**
  - O prompt cuida do que o código não consegue: recusar assuntos, pedir
    esclarecimento e manter o tom.
  - A mensagem fixa evita respostas "parciais" ("não posso, mas a capital é Paris...")
    e facilita verificar a recusa nos testes.
  - O prompt também lista explicitamente o que **não** existe (saque, extrato...),
    para o modelo não prometer funcionalidades.
- **Texto completo:** [`src/agente_bancario/agent/prompt.py`](src/agente_bancario/agent/prompt.py).

## DT-10 — Guardas determinísticas antes do LLM

- **Decisão:** mensagens vazias ou com mais de 1000 caracteres recebem uma resposta
  fixa, sem chamar o modelo.
- **Por quê:** economiza chamadas e reduz a superfície para jailbreaks longos (os
  ataques de "prompt gigante"). Também são comportamentos 100% previsíveis e
  testáveis.

## DT-11 — `TurnGuard` contra chamadas duplicadas

- **Decisão:** dentro de uma mesma mensagem do usuário, uma operação idêntica
  (mesmo tipo, valor e destinatário) só executa uma vez. O guard é reiniciado a
  cada nova mensagem.
- **Por quê:** LLMs às vezes repetem uma chamada de ferramenta. Em um banco, isso
  seria um depósito ou uma transferência em dobro. Se o usuário realmente quiser
  repetir, o modelo pede confirmação e a operação acontece na mensagem seguinte.
- **Detalhe:** só operações **bem-sucedidas** são registradas. Uma tentativa com
  valor inválido seguida de uma com valor válido funciona normalmente.

## DT-12 — Lock nas ferramentas

- **Decisão:** um `threading.Lock` serializa a execução das ferramentas.
- **Por quê:** quando o Gemini pede várias chamadas de uma vez, o LangGraph pode
  executá-las em threads paralelas. Sem o lock, duas transferências poderiam ler o
  mesmo saldo ao mesmo tempo (race condition) e ambas passar na validação.

## DT-13 — Limite de recursão e tratamento de falhas

- **Decisão:**
  - `recursion_limit=12` por mensagem.
  - Qualquer exceção no loop do agente (API fora do ar, cota, rede) vira uma
    mensagem segura, e o erro é registrado no log.
- **Por quê:** impede loops infinitos entre o modelo e as ferramentas. Em caso de
  falha, o agente nunca inventa um resultado. Ele orienta o usuário a consultar o
  saldo, porque uma operação pode ter sido concluída antes da falha.

## DT-14 — Estado em memória, por sessão

- **Decisão:** cada sessão do Streamlit tem seu próprio `InMemoryAccountRepository`
  e seu próprio `BankAgent`, guardados em `st.session_state`.
- **Por quê:**
  - Atende ao requisito "persistir o saldo entre mensagens da mesma sessão" e isola
    os usuários entre si.
  - Segue a dica do enunciado: "comece com um saldo fixo e só depois pense em
    persistência mais sofisticada".
  - Como os casos de uso dependem da interface `AccountRepository`, trocar por
    SQLite ou Redis exige apenas uma nova classe com `get`/`save`.
- **Histórico da conversa:** fica no `BankAgent`, para dar contexto ao modelo. O
  **saldo não depende desse histórico**: ele vive no repositório.

## DT-15 — Streamlit com tema próprio

- **Decisão:** usar Streamlit com CSS próprio (`ui/styles.css`) e tema em
  `.streamlit/config.toml`, no layout "neobank violeta". Ele tem:
  - barra lateral com o saldo e as movimentações;
  - atalhos de ação;
  - balões de chat;
  - recibos;
  - cores por tipo de resposta.
- **Por quê:** o Streamlit permite uma interface visual em Python puro, sem um
  front-end separado. O layout foi escolhido entre três propostas, com base em
  padrões de apps de fintech: saldo em destaque, ações próximas e feedback visual
  para cada operação.
- **Segurança:** todo texto do usuário ou do modelo passa por `html.escape` antes de
  virar HTML (`ui/render.py`).

## DT-16 — Recibos gerados a partir da transação real

- **Decisão:** depois de uma operação, a interface compara o histórico de transações
  antes e depois da mensagem e monta o recibo com os **dados reais** da transação.
  O saldo da barra lateral também é lido direto da conta.
- **Por quê:** a interface vira uma auditoria visual. Se o modelo escrevesse um valor
  diferente do real, a divergência apareceria na tela.
- **Detalhe:** quando todas as operações deram certo, o recibo substitui o texto do
  modelo. Se alguma ferramenta retornou `ERRO:`, o texto do modelo também aparece,
  para explicar o erro.

## DT-17 — TDD e duas camadas de teste

- **Decisão:**
  - Escrever os testes antes da implementação (Red → Green → Refactor).
  - Separar duas camadas:
    - **unitária:** sem LLM, roda sempre;
    - **ponta a ponta:** contra o Gemini real, marcada com `@pytest.mark.e2e` e
      fora da execução padrão.
- **Por quê:** as regras de negócio precisam de testes rápidos e determinísticos. O
  comportamento do LLM (recusas, jailbreak) só pode ser verificado com o modelo de
  verdade. Os testes e2e são mais lentos e gastam cota, por isso rodam sob demanda.
- **Detalhe:** os testes e2e verificam o **estado real da conta** e as ferramentas
  chamadas, não só o texto da resposta.

## DT-18 — `uv` para ambiente e dependências

- **Decisão:** gerenciar Python (3.12), o ambiente virtual e as dependências com
  [uv](https://docs.astral.sh/uv/). Versões fixadas em `uv.lock`.
- **Por quê:** um único comando (`uv sync`) instala a versão certa do Python e as
  versões exatas das dependências, e garante que o projeto rode igual em qualquer
  máquina.
- **Por que Python 3.12:** é a versão estável mais compatível com o ecossistema
  LangChain no momento do projeto.

## DT-19 — Chave de API fora do código

- **Decisão:** a chave vem da variável de ambiente `GEMINI_API_KEY` (ou
  `GOOGLE_API_KEY`), opcionalmente a partir de um arquivo `.env`, que está no
  `.gitignore`. O repositório traz só o `.env.example`.
- **Por quê:** a chave nunca vai para o GitHub. Se ela não existir, a interface
  mostra uma mensagem clara em vez de quebrar.
- **Localização do `.env`:** o `load_dotenv()` procura o arquivo a partir da pasta
  do projeto, subindo pelas pastas acima. Como o projeto vive dentro do repositório
  `formacao-especialista-em-ia`, a chave pode ficar:
  - em `projeto-agente-financeiro/.env`, que tem prioridade;
  - ou no `.env` da raiz do repositório, compartilhado com os outros cursos.

[← Voltar ao README](README.md)
