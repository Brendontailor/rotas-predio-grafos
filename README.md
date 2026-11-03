# Rotas do Prédio - UNISENAC

**Unidade Curricular:** Algoritmos e Estruturas de Dados II  
**Professor:** Pablo De Chiaro

## Integrantes

- Brendon Tailor, Leonardo Rosler e Conrado Soares

## Unidade dos pesos

As distâncias das arestas estão em metros. Cada peso representa somente a distância entre duas portas vizinhas. O custo de uma rota é a soma dos pesos das arestas percorridas.

## Arquivos (entregáveis obrigatórios)

- `arestas.txt`: ligações entre as portas e suas distâncias (uma por linha, metros).
- `grafo.py`: carrega as arestas e monta a lista de adjacência bidirecional.
- `buscas.py`: implementa BFS, DFS, busca gulosa e Dijkstra — todos retornam `(caminho, custo, visitados)`.
- `api.py`: API FastAPI com 4 endpoints obrigatórios.
- `desenho_grafo.png`: desenho do grafo (1920×1080) gerado a partir dos dados.
- `README.md`: este arquivo.

## Como executar

Instale as dependências:

```bash
pip install fastapi uvicorn
```

Inicie a API:

```bash
uvicorn api:app --reload
```

Acesse `http://127.0.0.1:8000/docs` para testar os endpoints no Swagger UI.

## Endpoints (aparecem no `/docs`)

- `GET /portas`: lista todas as 35 portas em ordem alfabética.
- `GET /vizinhos/{porta}`: mostra os vizinhos e o peso (metros) de cada ligação. Porta inexistente → **404 "Porta não encontrada."**
- `GET /rota?origem=X&destino=Y&algoritmo=Z`: calcula rota. `algoritmo` ∈ `{bfs, dfs, gulosa, dijkstra}`. Porta inexistente → **404**.
- `GET /comparar?origem=X&destino=Y`: executa os 4 algoritmos e devolve lado a lado (caminho, custo, visitados).

## Diferença entre BFS e Dijkstra

Para a rota de `LAB_TEC` até `PATIO_3`:

- **BFS:** `LAB_TEC -> PATIO_1 -> PATIO_3`, com custo de 33 metros.
- **Dijkstra:** `LAB_TEC -> SALA_201 -> SALA_203 -> PATIO_2 -> PATIO_3`, com custo de 31 metros.

A BFS encontra um caminho com menos arestas, sem considerar os pesos durante a busca. Dijkstra considera o peso de cada ligação e encontra o menor custo total.

## Conferência

Cada ligação aparece uma única vez em `arestas.txt`. O programa cria automaticamente a ligação de volta na lista de adjacência.

## Desenho manual

As fotos do desenho do grafo feito no caderno estão no repositório como entregáveis complementares.
