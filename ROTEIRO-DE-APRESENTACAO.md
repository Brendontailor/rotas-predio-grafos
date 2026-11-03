# Roteiro de Apresentação — Rotas do Prédio (UNISENAC)

**UC:** Algoritmos e Estruturas de Dados II
**Professor:** Pablo De Chiaro
**Integrantes:** Brendon Tailor, Leonardo Rosler e Conrado Soares

---

## 1. Pré-requisitos (verificar antes da apresentação)

- Python 3.10+ instalado — confirmar com `python --version`
- Dependências: `fastapi` e `uvicorn` (já vêm no `requirements.txt`)

```bash
python --version
pip install -r requirements.txt
```

> Se `python` não funcionar no terminal do professor, use `python3` ou o caminho completo
> do executável (Windows: `where python`).

---

## 2. Passo a passo para rodar

### Passo 1 — Abrir o terminal na pasta do projeto

```bash
cd caminho/para/atividade-grafos
```

### Passo 2 — (Opcional, mas recomendado) Criar um ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
```

### Passo 3 — Subir a API

```bash
uvicorn api:app --reload
```

Saída esperada:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Passo 4 — Abrir o Swagger no navegador

Acesse: **http://127.0.0.1:8000/docs**

> `--reload` reinicia o servidor sozinho quando um arquivo muda. Para encerrar: `CTRL + C`.

---

## 3. Roteiro do que falar (ordem sugerida)

### 3.1 O problema

Modelamos o prédio da UNISENAC como um **grafo ponderado e não direcionado**:

- **Vértices:** 35 portas do prédio
- **Arestas:** 46 ligações entre portas vizinhas
- **Peso:** distância em metros entre duas portas vizinhas

O objetivo é responder: *"qual o caminho mais curto entre a porta X e a porta Y?"*

### 3.2 Como o grafo é montado (`grafo.py`)

- `arestas.txt` tem uma ligação por linha: `ORIGEM DESTINO PESO`
- Exemplo: `SALA_201 LAB_TEC 3` (3 metros)
- O arquivo lista **cada ligação apenas uma vez**; o `carregar_grafo` cria automaticamente
  a aresta de volta → **lista de adjacência bidirecional**
- Validações feitas na carga: exatamente 3 campos por linha, peso numérico e peso > 0

### 3.3 Os quatro algoritmos (`buscas.py`)

Todos retornam a mesma assinatura: **`(caminho, custo, visitados)`**

| Algoritmo | Estrutura | Prioridade | Garante o menor custo? |
|---|---|---|---|
| BFS | Fila (FIFO) / `deque` | Nº de arestas | Não — ignora os pesos |
| DFS | Pilha (LIFO) | Profundidade | Não |
| Gulosa | Heap | Peso da **aresta imediata** | Não — olha custo local, não global |
| Dijkstra | Heap | Custo **total acumulado** | **Sim** (pesos positivos) |

Detalhe que vale destacar: na Gulosa o heap usa `(peso, ordem, vizinho)`. O `ordem` é um
contador de inserção que serve para **desempatar de forma estável** (ordem de descoberta)
em vez de deixar o Python desempatar alfabeticamente pelo nome da porta. Assim dois
caminhos com o mesmo custo sempre saem na mesma ordem, e o resultado é reprodutível.

### 3.4 A API (`api.py`) — FastAPI com 4 endpoints

| Endpoint | O que faz |
|---|---|
| `GET /portas` | Lista as 35 portas em ordem alfabética |
| `GET /vizinhos/{porta}` | Vizinhos + peso de cada ligação |
| `GET /rota?origem=&destino=&algoritmo=` | Calcula a rota com o algoritmo escolhido |
| `GET /comparar?origem=&destino=` | Roda os 4 algoritmos lado a lado |

- Porta inexistente → **404 "Porta não encontrada."**
- Sem caminho → **404 "Não existe caminho entre as portas."**
- O grafo é carregado **uma única vez** no startup (não a cada requisição)

---

## 4. Demonstração ao vivo (com resultados reais já verificados)

### Demo 1 — O caso canônico: `LAB_TEC` → `PATIO_3`

```
http://127.0.0.1:8000/comparar?origem=LAB_TEC&destino=PATIO_3
```

| Algoritmo | Caminho | Custo | Visitados |
|---|---|---|---|
| BFS | LAB_TEC → PATIO_1 → PATIO_3 | **33,0 m** | 5 |
| DFS | LAB_TEC → SALA_201 → SALA_203 → PATIO_2 → PATIO_3 | **31,0 m** | 24 |
| Gulosa | LAB_TEC → SALA_201 → SALA_203 → PATIO_2 → PATIO_3 | **31,0 m** | 24 |
| Dijkstra | LAB_TEC → SALA_201 → SALA_203 → PATIO_2 → PATIO_3 | **31,0 m** | 10 |

**Frase pronta:** *"A BFS achou o caminho com menos arestas (2), mas não o mais curto em metros.
São 33 m. A Dijkstra achou 4 arestas, mas 31 m — 2 metros mais barato. Isso prova que,
em grafo ponderado, minimizar número de arestas ≠ minimizar custo."*

### Demo 2 — Onde a Gulosa falha (o ponto mais forte da apresentação)

```
http://127.0.0.1:8000/comparar?origem=APOIO_TEC&destino=CANTINA_2
```

| Algoritmo | Custo | Visitados |
|---|---|---|
| BFS | 48,7 m | 17 |
| DFS | 48,7 m | 31 |
| **Gulosa** | **54,1 m** ❌ | 18 |
| Dijkstra | **48,7 m** ✅ | 19 |

**Por que a Gulosa erra:** ela escolhe sempre a aresta **mais barata na hora**. Saindo de
`APOIO_TEC`, ela vai por `MASSAGISTA` e cai no "beco sem saída" `SECRETARIA → COORDENACAO →
DIEREÇÃO → PEDAGOGIA → SALA_PROF → BIBLIOTECA`, refazendo um trecho longo. A Dijkstra
considera o **custo acumulado** e vai direto por `BANHEIRO_MASCULINO → BANHEIRO_FEMININO → PATIO_2`.

> Em varredura completa, existem **215 pares de portas** em que a Gulosa não é ótima —
> prova de que ela não garante a solução ótima global.

### Demo 3 — Dijkstra com custo bem menor que BFS

```
http://127.0.0.1:8000/comparar?origem=APOIO_TEC&destino=PATIO_1
```

| Algoritmo | Custo | Visitados |
|---|---|---|
| BFS | 77,8 m | 22 |
| DFS | 67,6 m | 12 |
| Gulosa | 66,7 m | 27 |
| **Dijkstra** | **57,3 m** ✅ | 24 |

**Frase pronta:** *"A diferença de 20,5 m entre BFS e Dijkstra mostra o custo de ignorar os
pesos. Repare também que a DFS visitou menos vértices (12) e ainda assim não encontrou o
melhor caminho — visitar menos não é sinônimo de encontrar a melhor rota."*

> Observação honesta se o professor perguntar: Dijkstra visitou 24 vértices, mais que a DFS
> (12). Isso é esperado — o heap do Dijkstra exige expandir parcialmente a fronteira para
> poder priorizar pelo custo acumulado.

### Demo 4 — Tratamento de erro (mostrar que a API valida)

```
http://127.0.0.1:8000/vizinhos/PORTA_QUE_NAO_EXISTE
```
→ `404 {"detail":"Porta não encontrada."}`

---

## 5. Dados do grafo para citar

- **35 portas**, **46 arestas**
- Grafo **totalmente conexo** (partindo de qualquer porta, alcança-se todas as outras)
- Existe **outro caminho** entre as portas do corredor central — é isso que faz os algoritmos
  discordarem entre si
- **380 pares de portas** têm BFS e Dijkstra com custos diferentes

---

## 6. Perguntas prováveis do professor e como responder

| Pergunta | Resposta |
|---|---|
| Por que a lista de adjacência e não matriz de adjacência? | O grafo é esparso (46 arestas para 35 vértices). A lista usa O(V+E) de memória contra O(V²) da matriz. |
| Complexidade de cada algoritmo? | BFS e DFS: **O(V+E)**. Gulosa e Dijkstra: **O(E·log V)** com heap binário. |
| Por que Dijkstra funciona aqui? | Todos os pesos são **estritamente positivos** (validados na carga do arquivo), que é a precondition do algoritmo. |
| O que acontece com peso negativo? | Dijkstra deixaria de ser válido — o custo finalizado poderia melhorar depois. O `carregar_grafo` já rejeita pesos ≤ 0. |
| Como a API sabe o caminho? | Cada busca guarda um dicionário `anterior` ligando cada vértice ao predecessor; ao chegar no destino, o `reconstruir_caminho` volta pela cadeia e inverte a lista. |
| Por que `--reload`? | Recarrega o servidor a cada mudança no código, permitindo demonstrar ajustes ao vivo durante a apresentação. |
| O grafo é direcionado? | Não. `arestas.txt` lista cada ligação uma vez e o código insere a aresta nos dois sentidos. |
| O grafo tem ciclos? | Sim, e é por isso que cada busca mantém um conjunto de visitados para não entrar em laço infinito. |

---

## 7. Checklist final

- [ ] `python --version` responde sem erro
- [ ] `pip install -r requirements.txt` executado
- [ ] `uvicorn api:app --reload` sobe sem traceback
- [ ] `http://127.0.0.1:8000/docs` abre no navegador
- [ ] Testar `/portas`, `/vizinhos/{porta}`, `/rota` e `/comparar`
- [ ] Testar o erro 404 com uma porta inexistente
- [ ] `desenho_grafo.png` aberto para mostrar o grafo desenhado
- [ ] Fotos do desenho no caderno prontas (arquivos complementares no repositório)

---

## 8. Comandos prontos para colar

```bash
pip install -r requirements.txt
uvicorn api:app --reload
```

```bash
# Testes rápidos em outra aba do terminal
curl "http://127.0.0.1:8000/portas"
curl "http://127.0.0.1:8000/vizinhos/LAB_TEC"
curl "http://127.0.0.1:8000/rota?origem=LAB_TEC&destino=PATIO_3&algoritmo=bfs"
curl "http://127.0.0.1:8000/rota?origem=LAB_TEC&destino=PATIO_3&algoritmo=dijkstra"
curl "http://127.0.0.1:8000/comparar?origem=APOIO_TEC&destino=CANTINA_2"
```
