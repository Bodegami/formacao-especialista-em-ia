# AI Specialist Program — Study Portfolio

**Santander Open Academy × Alura · _Formação Especialista em IA_**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?logo=langgraph&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?logo=googlegemini&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-F97316?logo=gradio&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-EA4B71?logo=n8n&logoColor=white)

This repository documents my path through the **AI Specialist** program offered by
**Santander Open Academy** in partnership with **Alura**: **30 courses and 231 hours**
of study between **April and November 2026**, split into a foundation track and an
advanced track, with weekly live classes.

The program goes from computational thinking and Python all the way to
production-minded LLM applications: classic AI, machine learning, fine-tuning,
Hugging Face models, RAG pipelines with evaluation, multi-agent systems with memory
and human-in-the-loop, workflow automation, and AI governance.

Every course that involved code lives in its own folder, with the notebooks and
scripts I wrote along the way. The program ends with a **capstone project**: a
restricted banking agent built with clean architecture, TDD, and an adversarial test
suite against a real LLM.

---

## Table of contents

1. [Program overview](#program-overview)
2. [Highlights](#highlights)
3. [Skills map](#skills-map)
4. [Capstone project — Restricted Banking Agent](#capstone-project--restricted-banking-agent)
5. [Learning path](#learning-path)
6. [Tech stack](#tech-stack)
7. [Repository structure](#repository-structure)
8. [How to navigate and run](#how-to-navigate-and-run)

---

## Program overview

| Track | Period | Workload | Courses | Focus |
|---|---|---|---|---|
| **Foundation** — _Nivelamento_ | Apr 27 – Jun 26, 2026 | 98 h | 14 | Computational thinking, Python, data analysis, generative AI, prompt engineering, classic AI, and machine learning fundamentals |
| **Advanced** — _Boost_ | Jul 8 – Nov 20, 2026 | 133 h | 16 | Automation with n8n, OpenAI API, fine-tuning, LangChain, RAG, LangGraph agents, Hugging Face, AI web apps, governance, and AI for business |
| **Total** | **Apr – Nov 2026** | **231 h** | **30** | Plus weekly live classes and the [capstone project](#capstone-project--restricted-banking-agent) |

All 30 courses were completed. **16 of them** produced code in this repository; the
others were conceptual or tool-based (prompting, no-code automation, governance,
business) and are listed in the [learning path](#learning-path) as _course only_.

---

## Highlights

- **Capstone: Restricted Banking Agent.** An LLM agent (LangChain + Gemini + Streamlit)
  that only checks balance, deposits, and transfers. Business rules live in code,
  not in the prompt. Clean Architecture, TDD, **96 unit tests** and **35 adversarial
  end-to-end scenarios** (jailbreaks, off-topic requests, invalid amounts), all passing.
- **RAG from basics to advanced, with evaluation.** Five vector stores, hybrid search
  (BM25 + vectors), multi-vector retrieval, query transformations (Multi-Query,
  Step-Back, HyDE), embedding caching, and quality measured with **RAGAS** and **LangSmith**.
- **Multi-agent systems with LangGraph.** ReAct agents, persistence and streaming,
  **human-in-the-loop** approvals, a planner/researcher/writer/critic essay team,
  and an email assistant with **long-term semantic memory** (LangMem).
- **Model training and publishing.** Transfer learning of a Portuguese DistilBERT to
  grade essays, **published on the Hugging Face Hub**, plus hands-on use of
  fine-tuned **GPT-4o** models through the OpenAI API.
- **Solid foundations.** Classic AI (expert systems, Bayesian networks, Markov chains,
  A\* search), supervised and unsupervised ML, CNNs, and reinforcement learning (Q-Learning).
- **Beyond code.** Prompt engineering, workflow automation with **n8n**, AI-built web
  apps with **Lovable + Supabase**, and **AI governance and compliance** (LGPD, GDPR, EU AI Act).

---

## Skills map

📁 = code in this repository · 📘 = course only (no code here)

| Area | What I practiced | Where to look |
|---|---|---|
| **Programming foundations** | Computational thinking, logic, data types, collections, control flow, functions, lambdas, recursion, closures, exception handling | 📘 [Computational thinking](#f1-computational-thinking) · 📁 [Python for Data](python-para-dados-primeiros-passos/), [Practicing Python](#f7-practicing-python--conditionals) |
| **Data analysis** | Exploratory analysis with Pandas and NumPy, charts with Matplotlib, Seaborn, and Plotly | 📁 [Pandas](python-com-pandas/), [Python for Data](python-para-dados-funcoes-collections/) |
| **Generative AI and prompt engineering** | Prompting techniques, ChatGPT, Gemini and Google AI Studio, system prompts, few-shot, structured outputs with Pydantic, scope restriction and refusal, guardrails | 📘 [Prompt Engineering](#f4-prompt-engineering), [ChatGPT](#f6-chatgpt-optimizing-results) · 📁 [LangChain + OpenAI](langchain-criando-ferramentas-com-openai/), [Capstone](projeto-agente-financeiro/) |
| **Classic AI** | Intelligent agents, state spaces, expert system with forward-chaining inference, Bayesian network, Markov chain, A\* search | 📁 [AI Fundamentals](fundamentos-de-ia/) |
| **Machine learning** | Decision trees, KNN, linear/logistic regression, Random Forest, GridSearchCV, cross-validation, K-Means, PCA | 📁 [ML Algorithms](machine-learning-algorimos/) |
| **Deep learning and RL** | CNN with Keras, transfer learning with MobileNetV2, Q-Learning on Gymnasium FrozenLake | 📁 [ML Algorithms](machine-learning-algorimos/) |
| **LLM APIs** | OpenAI (parameters, assistants, threads, cost), Google Gemini, Groq (Llama 3.1), local models with Ollama and LM Studio (Gemma 3), structured JSON output | 📘 [GPT and Python](#a3-gpt-and-python--building-tools-with-the-api) · 📁 [Applied AI](python-ia-aplicada/), [LangChain courses](#advanced-track--boost) |
| **Fine-tuning** | JSONL dataset format for chat fine-tuning, train/validation split, calling fine-tuned GPT-4o models via the OpenAI API | 📁 [Fine-tuning](python-fine-tuning/) |
| **Hugging Face** | Pipelines, sentiment analysis, zero-shot classification, extractive QA, image background removal, transfer learning, publishing to the Hub | 📁 [Exploring HF](hf-explorando-e-aplicando-solucoes-com-ia/), [Transfer Learning](hf-transferindo-aprendizado-modelos-nlp/) |
| **Embeddings and semantic search** | Cosine similarity, Gemini vs. local Hugging Face embeddings, batch indexing | 📁 [Chatbots and RAG](langchain-criando-chatbots-e-rag/) |
| **Caching** | Embedding cache with `CacheBackedEmbeddings` + `LocalFileStore` to cut cost and latency | 📁 [Chatbots and RAG — Lesson 3](langchain-criando-chatbots-e-rag/Aula_03_embeddings_alta_performance.ipynb) |
| **Vector databases** | FAISS, Chroma, Pinecone, Milvus, in-memory stores | 📁 [Chatbots and RAG](langchain-criando-chatbots-e-rag/), [Advanced RAG](langchain-tecnicas-avancadas-rag/) |
| **RAG** | Ingestion pipelines (PDF, SQL with DuckDB), chunking strategies, hybrid search, multi-vector, Multi-Query, Step-Back, HyDE, conversational memory, re-ranking | 📁 [Chatbots and RAG](langchain-criando-chatbots-e-rag/), [Advanced RAG](langchain-tecnicas-avancadas-rag/) |
| **RAG evaluation** | RAGAS (faithfulness, answer relevancy, context precision and recall), LangSmith tracing, QAEvalChain | 📁 [Chatbots and RAG — Lesson 6](langchain-criando-chatbots-e-rag/Aula_06_notebook_avaliacao_langsmith_ragas.ipynb) |
| **Agents** | Function calling / tool use, ReAct, routers, web search tools (Tavily, DuckDuckGo) | 📁 [LangGraph](langgraph-orchestrando-agentes-e-multi-agentes/), [Capstone](projeto-agente-financeiro/) |
| **Multi-agent and memory** | LangGraph state graphs, conditional edges, SQLite checkpoints, streaming, human-in-the-loop, triage routing, LangMem semantic memory | 📁 [LangGraph](langgraph-orchestrando-agentes-e-multi-agentes/) |
| **Workflow automation** | No-code/low-code process automation with n8n, integrating services and LLMs with conditional logic | 📘 [n8n courses](#a1-flash-skills-process-automation-with-n8n-and-ai) |
| **AI app interfaces and web apps** | Gradio and Streamlit chat apps; AI-built web apps with Lovable, Supabase, and React | 📁 [Hugging Face courses](#a9-hugging-face--exploring-and-applying-ai-models), [Capstone](projeto-agente-financeiro/) · 📘 [Lovable](#a14-lovable-building-web-applications-with-ai) |
| **AI governance and ethics** | Responsible AI, compliance, and regulation (LGPD, GDPR, EU AI Act) | 📘 [AI Governance](#a12-ai-governance-ethical-strategies-and-compliance) |
| **AI for business** | Market readiness and portfolio, AI-driven business models, AI-assisted negotiation, data-driven decision-making | 📘 [Business courses](#a11-ai-getting-ready-for-the-job-market) |
| **Software engineering** | Clean Architecture, TDD, unit + adversarial E2E tests, `uv` environments, technical documentation | 📁 [Capstone](projeto-agente-financeiro/) |

---

## Capstone project — Restricted Banking Agent

📁 [`projeto-agente-financeiro/`](projeto-agente-financeiro/)

An AI agent that manages a fictional bank account (initial balance: R$ 1,000.00)
and allows **only three operations**: check balance, deposit, and transfer. It must
make **zero calculation errors** and refuse **everything** outside that scope.

**Core principle: the LLM interprets, the code decides.** The model only turns natural
language into tool calls. Validation, math, and balance changes happen in code, so
even a jailbroken model cannot break the rules.

- **Stack:** Python 3.12, LangChain 1.x (`create_agent`), Google Gemini, Streamlit, pytest, uv
- **Architecture:** Clean Architecture (domain → use cases → infrastructure → adapters)
- **Reliability:** `Decimal` money, strict input parsing (rejects ambiguous formats like `1.000`), atomic operations, duplicate-call guard, lock against parallel tool calls
- **Security:** hardened system prompt, fixed refusal message, input guards before the LLM, HTML escaping in the UI
- **Tests:** 96 unit tests + 35 adversarial E2E scenarios against the real model, asserting on the **actual account state**, not just the text
- **Docs:** [README](projeto-agente-financeiro/README.md) · [Business rules](projeto-agente-financeiro/REGRAS_DE_NEGOCIO.md) · [Technical decisions](projeto-agente-financeiro/DECISOES_TECNICAS.md) (in Portuguese)

### 🎬 Demo video

▶️ Video: 

https://github.com/user-attachments/assets/21991fd4-2cad-4a67-a1ff-1c3dccd9c9e8


 <!-- Replace "_coming soon_" with the link, e.g. [Watch the demo](https://...) -->

---

## Learning path

All 30 courses, in the official order of each track. Original Portuguese titles are
in italics.

- 📁 **Code in this repo:** the course has its own folder and its own branch
  (`course/...` or `challenges/...`) with a lesson-by-lesson commit history.
- 📘 **Course only:** a conceptual or tool-based course with no code in this repository.

### Foundation track — _Nivelamento_

**Apr 27 – Jun 26, 2026 · 98 hours · 14 courses**

#### F1. Computational thinking
_Pensamento computacional: fundamentos da computação e lógica de programação_ · 📘 Course only

Computing fundamentals, programming logic, how software is structured, and how
programs interact with the operating system.

#### F2. Exploring the potential of generative AI
_IA: explorando o potencial da inteligência artificial generativa_ · 📘 Course only

Generative AI concepts and tools for producing text, summaries, and multimodal
content, along with their applications and limitations.

#### F3. Python for Data — first steps
_Python para Dados: primeiros passos_ · 📁 [`python-para-dados-primeiros-passos/`](python-para-dados-primeiros-passos/)

- **Concepts:** variables and types, strings, operators, truth tables, control flow, `break`/`continue`.
- **Practice:** hands-on notebooks in Google Colab, data collection and sampling exercises.

#### F4. Prompt engineering
_Engenharia de Prompt: criando prompts eficazes para IA Generativa_ · 📘 Course only

Techniques for writing effective prompts for generative AI models.

#### F5. Python for Data — functions, data structures, and exceptions
_Python para Dados: trabalhando com funções, estruturas de dados e exceções_ · 📁 [`python-para-dados-funcoes-collections/`](python-para-dados-funcoes-collections/)

- **Concepts:** libraries, built-in and custom functions, lambdas, lists, dictionaries, exception handling.
- **Practice:** student-grade analysis and random selection with Matplotlib and `random`.

#### F6. ChatGPT: optimizing results
_ChatGPT: otimizando a qualidade dos resultados_ · 📘 Course only

Improving the quality and reliability of ChatGPT outputs through better instructions,
context, and iteration.

#### F7. Practicing Python — conditionals
_Praticando Python: condicionais if, elif e else_ · 📁 [`python-exercicios-condicionais/`](python-exercicios-condicionais/)

10 real-world problems: toll calculation, BMI, loan approval, student grading, budget
control, server temperature monitoring, and office access control.

#### F8. Practicing Python — loops
_Praticando Python: laços for e while_ · 📁 [`python-exercicios-loops/`](python-exercicios-loops/)

10 problems on `for`/`while`, `break`/`continue`, and infinite loops: countdowns,
inventory control, and login validation.

#### F9. Learning: personalizing your study routine with ChatGPT
_Aprendizagem: personalizando sua rotina de estudos com ChatGPT_ · 📘 Course only

Using ChatGPT as a study assistant to plan, organize, and personalize a learning routine.

#### F10. Practicing Python — functions
_Praticando Python: funções_ · 📁 [`python-exercicios-funcoes/`](python-exercicios-funcoes/)

10 problems: lambdas, recursion, closures, function factories, type conversion, and
list manipulation.

#### F11. Pandas: getting to know the library
_Pandas: conhecendo a biblioteca_ · 📁 [`python-com-pandas/`](python-com-pandas/)

- **Concepts:** loading datasets, exploratory data analysis, filtering, cleaning, exporting.
- **Practice:** real-estate dataset analysis, with lesson challenges and filtered CSV outputs.

#### F12. Python: Applied Artificial Intelligence
_Python: Inteligência Artificial Aplicada_ · 📁 [`python-ia-aplicada/`](python-ia-aplicada/)

- **Concepts:** calling LLM APIs from Python, system prompts, file I/O, data generation with Faker.
- **Practice:**
  - Called cloud LLMs (**Gemini**, **Groq / Llama 3.1**) from notebooks.
  - Ran a **local LLM** (Gemma 3 4B) behind an OpenAI-compatible server (LM Studio).
  - Final challenge: a pipeline that reads app reviews, has the local model convert
    each one into **structured JSON** with a sentiment label, and aggregates the results.

#### F13. AI Fundamentals: structure and approaches of intelligent systems
_Fundamentos de IA: explorando a estrutura e abordagens de sistemas inteligentes_ · 📁 [`fundamentos-de-ia/`](fundamentos-de-ia/)

- **Concepts:** intelligent agents, state spaces, search, logical and probabilistic reasoning.
- **Practice:**
  - **Expert system** with a knowledge base and forward-chaining inference (diagnosis helper).
  - **Bayesian network** to estimate purchase probability from customer behavior.
  - **Markov chain** for weather forecasting.
  - **A\* search** for product recommendation.

#### F14. AI Fundamentals: machine learning algorithms and approaches
_Fundamentos de IA: investigando algoritmos e abordagens de machine learning_ · 📁 [`machine-learning-algorimos/`](machine-learning-algorimos/)

- **Supervised learning:** decision trees, KNN, linear and logistic regression, Random Forest (feature importance), confusion matrix.
- **Model tuning:** train/test split, cross-validation, **GridSearchCV**.
- **Unsupervised learning:** K-Means clustering, **PCA** for dimensionality reduction.
- **Deep learning:** CNN with Keras, transfer learning with **MobileNetV2**, image preprocessing with OpenCV.
- **NLP:** bag-of-words and Transformers pipelines.
- **Reinforcement learning:** **Q-Learning** agent crossing the Gymnasium FrozenLake.

### Advanced track — _Boost_

**Jul 8 – Nov 20, 2026 · 133 hours · 16 courses**

#### A1. Flash Skills: process automation with n8n and AI
_Flash Skills: automação de processos com n8n e IA_ · 📘 Course only

Introduction to building automated workflows with n8n and AI services.

#### A2. Workflow automation: integrating n8n and AI
_Automação de Fluxos: integrando n8n e IA_ · 📘 Course only

Intelligent automations that integrate external services, LLMs, and analyses using
conditional logic.

#### A3. GPT and Python — building tools with the API
_GPT e Python: criando ferramentas com a API_ · 📘 Course only

Building tools on the OpenAI API: model parameters, assistants, threads, and
cost best practices.

#### A4. Fine-Tuning OpenAI: customizing GPT models
_Fine-Tuning OpenAI: personalize seus modelos GPT_ · 📁 [`python-fine-tuning/`](python-fine-tuning/)

- **Concepts:** fine-tuning dataset format (JSONL chat examples), train/validation split, iterating on data quality.
- **Practice:** studied the JSONL training and validation datasets (two iterations)
  used to fine-tune **GPT-4o**, and ran the course scripts locally against the
  fine-tuned models to profile movie-forum users and generate marketing recommendations.

#### A5. LangChain — building smart chatbots with RAG
_LangChain: criando chatbots inteligentes com RAG_ · 📁 [`langchain-criando-chatbots-e-rag/`](langchain-criando-chatbots-e-rag/)

The most extensive RAG course, built on **Google Gemini**:

| Lesson | Topic |
|---|---|
| 1 | RAG architecture in practice: traditional prompting vs. RAG |
| 2 | Vector storage with **FAISS, Chroma, and Pinecone**, documents with metadata |
| 3 | High-performance embeddings: Gemini vs. local Hugging Face, **embedding cache**, batch processing |
| 4 | Pipelines for complex data: PDFs with Unstructured, **SQL with DuckDB**, smart chunking |
| 5 | Robust conversation chains: memory, **guardrails**, re-ranking |
| 6 | Evaluation with **LangSmith and RAGAS** (faithfulness, answer relevancy, context precision and recall) |
| 7 | Advanced techniques: **hybrid search** (BM25 + vectors) and **multi-vector retrieval** |
| 8 | **Capstone:** expert RAG assistant: ETL → hybrid retrieval → conversational chain → RAGAS evaluation |

#### A6. LangChain and Python — building tools with OpenAI
_LangChain e Python: criando ferramentas com a OpenAI_ · 📁 [`langchain-criando-ferramentas-com-openai/`](langchain-criando-ferramentas-com-openai/)

- **Concepts:** LCEL chains, prompt templates, output parsers, structured output with **Pydantic**, per-session chat history.
- **Practice:** a travel assistant with structured outputs, a chat with memory, RAG over
  text and multiple PDFs with **FAISS**, and a first **LangGraph** router that sends
  each request to a specialized node (async).

#### A7. LangChain — advanced RAG techniques
_LangChain: Técnicas Avançadas de RAG_ · 📁 [`langchain-tecnicas-avancadas-rag/`](langchain-tecnicas-avancadas-rag/)

- **Concepts:** the RAG pipeline step by step, LangSmith debugging, query transformations.
- **Practice:**
  - **Rewrite-Retrieve-Read**, **Multi-Query**, **Step-Back prompting**, and **HyDE**
    (Hypothetical Document Embeddings), comparing results with and without each technique.
  - Local LLMs with **Ollama** (Gemma 3 1B vs. 4B) for query rewriting.
  - **Milvus** as a vector store, semantic chunking, and automated QA evaluation with `QAEvalChain`.

#### A8. LangGraph — orchestrating agents and multi-agent systems
_LangGraph: Orquestrando agentes e multiagentes_ · 📁 [`langgraph-orchestrando-agentes-e-multi-agentes/`](langgraph-orchestrando-agentes-e-multi-agentes/)

| Lesson | Topic |
|---|---|
| 1 | The **ReAct** pattern from scratch |
| 2 | LangGraph components: state, nodes, conditional edges |
| 3 | Search agents with **Tavily** and DuckDuckGo |
| 4 | **Persistence and streaming** with SQLite checkpoints and threads |
| 5 | **Human-in-the-loop**: interrupts, state inspection, and editing |
| 6 | Multi-agent orchestration: an essay team that **plans, researches, writes, and critiques**, with a Gradio app |
| 7 | Multi-agent systems with prebuilt ReAct agents, triage, and `Command` routing |
| 8 | Email assistant with **long-term semantic memory (LangMem)** and human-in-the-loop |

#### A9. Hugging Face — exploring and applying AI models
_Hugging Face: explorando e aplicando soluções com modelos de IA_ · 📁 [`hf-explorando-e-aplicando-solucoes-com-ia/`](hf-explorando-e-aplicando-solucoes-com-ia/)

- **Concepts:** choosing models on the Hub, pipelines, building demos.
- **Practice:**
  - **Sentiment analysis** of Portuguese reviews, with word clouds and Plotly charts.
  - **Zero-shot product categorization** (BART-MNLI and a multilingual T5).
  - **Image background removal**.
  - **Extractive question answering** (RoBERTa-SQuAD2).
  - An order-status **chatbot**, with **Gradio** interfaces throughout.

#### A10. Hugging Face — transfer learning for NLP models
_Hugging Face: transferindo aprendizado de modelos de NLP_ · 📁 [`hf-transferindo-aprendizado-modelos-nlp/`](hf-transferindo-aprendizado-modelos-nlp/)

- **Concepts:** transfer learning, tokenization, target preparation, loss metrics.
- **Practice:** fine-tuned a Portuguese **DistilBERT** (TensorFlow) to grade essays,
  **published it on the Hugging Face Hub** as
  [`devBode/distilbert-pt-cased-redacao-nota`](https://huggingface.co/devBode/distilbert-pt-cased-redacao-nota),
  and served predictions in a **Gradio** app.

#### A11. AI: getting ready for the job market
_Inteligência artificial: preparação para o mercado_ · 📘 Course only

Building a market-oriented AI portfolio and connecting AI projects to real business
problems. This repository is part of that effort.

#### A12. AI governance: ethical strategies and compliance
_Governança de IA: estratégias éticas e compliance nas empresas_ · 📘 Course only

Planning AI solutions with governance, ethics, and compliance in mind, including
data-protection and AI regulations (**LGPD**, **GDPR**, **EU AI Act**).

#### A13. Entrepreneurship with AI: from ideation to business model
_Empreendendo com IA: da ideação ao modelo de negócio_ · 📘 Course only

Integrating AI into product strategy, business models, and scalable operations.

#### A14. Lovable: building web applications with AI
_Lovable: criação de aplicações web com IA_ · 📘 Course only

Designing and publishing dynamic web applications with **Lovable**, **Supabase**,
**React**, and AI services.

#### A15. Negotiation: training skills with AI
_Negociação: treinando habilidades com IA_ · 📘 Course only

AI-assisted techniques to prepare for and practice negotiations.

#### A16. Decision-making with AI: optimizing strategies with data
_Tomada de decisão com IA: otimizando estratégias com dados_ · 📘 Course only

Using predictive models and data analysis to support business decisions.

### Capstone project

📁 [`projeto-agente-financeiro/`](projeto-agente-financeiro/). See [Capstone project](#capstone-project--restricted-banking-agent) above.

---

## Tech stack

| Category | Tools |
|---|---|
| **Language and environment** | Python, Jupyter / Google Colab, `uv`, `venv` |
| **Data** | Pandas, NumPy, Matplotlib, Seaborn, Plotly, DuckDB |
| **Machine learning** | scikit-learn, TensorFlow / Keras, OpenCV, Gymnasium |
| **LLM providers** | OpenAI (GPT-4o, GPT-4o-mini, GPT-4.1-nano), Google Gemini, Groq (Llama 3.1), local models with Ollama and LM Studio (Gemma 3) |
| **Generative AI tools** | ChatGPT, Google AI Studio, Gemini |
| **LLM frameworks** | LangChain, LangGraph, LangMem, LangSmith |
| **Hugging Face** | Transformers, Datasets, Hub, sentence-transformers embeddings |
| **Vector databases** | FAISS, Chroma, Pinecone, Milvus |
| **RAG evaluation** | RAGAS, LangSmith, QAEvalChain |
| **Agent tools** | Tavily, DuckDuckGo search |
| **Interfaces** | Streamlit, Gradio |
| **Automation and AI app builders** _(course only)_ | n8n, Lovable, Supabase |
| **Testing** | pytest (unit + adversarial E2E) |

---

## Repository structure

```
formacao-especialista-em-ia/
│   # Foundation track
├── python-para-dados-primeiros-passos/        # F3.  Python for Data — first steps
├── python-para-dados-funcoes-collections/     # F5.  Functions, data structures, exceptions
├── python-exercicios-condicionais/            # F7.  Practicing Python — conditionals
├── python-exercicios-loops/                   # F8.  Practicing Python — loops
├── python-exercicios-funcoes/                 # F10. Practicing Python — functions
├── python-com-pandas/                         # F11. Pandas
├── python-ia-aplicada/                        # F12. Python: Applied AI
├── fundamentos-de-ia/                         # F13. Classic AI
├── machine-learning-algorimos/                # F14. ML algorithms
│   # Advanced track
├── python-fine-tuning/                        # A4.  Fine-tuning with OpenAI
├── langchain-criando-chatbots-e-rag/          # A5.  Chatbots and RAG
├── langchain-criando-ferramentas-com-openai/  # A6.  LangChain tools with OpenAI
├── langchain-tecnicas-avancadas-rag/          # A7.  Advanced RAG
├── langgraph-orchestrando-agentes-e-multi-agentes/  # A8. LangGraph agents
├── hf-explorando-e-aplicando-solucoes-com-ia/ # A9.  Hugging Face models
├── hf-transferindo-aprendizado-modelos-nlp/   # A10. Transfer learning
│   # Capstone
└── projeto-agente-financeiro/                 # Restricted Banking Agent
```

### Branches

| Prefix | Content |
|---|---|
| `main` | Consolidated version of every course and the capstone |
| `course/<name>` | One branch per course, with a commit per lesson |
| `challenges/<name>` | Python exercise sets |
| `project/<name>` | Capstone project development |

---

## How to navigate and run

- **Notebooks (`.ipynb`)** were written for Jupyter or Google Colab. Most of them open
  and render directly on GitHub, outputs included.
- **Projects with a `requirements.txt`** can be set up with a virtual environment:

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- **The capstone project** uses `uv` and has a full step-by-step guide in its
  [README](projeto-agente-financeiro/README.md#7-run-como-executar).
- **API keys** (OpenAI, Gemini, Pinecone, Tavily, LangSmith...) are read from a
  `.env` file that is **never committed**. Create your own with the keys each course needs.

---

<sub>Course materials are the property of Alura and Santander Open Academy. The code,
notebooks, and solutions in this repository are my own work produced while taking the
program.</sub>
