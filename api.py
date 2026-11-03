# API para consultar portas, vizinhos e rotas do prédio.
# Usa FastAPI. Para rodar: uvicorn api:app --reload  ->  http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException, Query

from buscas import bfs, dfs, gulosa, dijkstra
from grafo import carregar_grafo
from pathlib import Path

app = FastAPI(title="Rotas do Prédio - UNISENAC")

# Carrega o grafo uma vez, a partir do arestas.txt que fica na mesma pasta.
caminho_arestas = Path(__file__).with_name("arestas.txt")
grafo = carregar_grafo(caminho_arestas)

# Dicionário que liga o nome do algoritmo (texto da URL) à função em buscas.py.
algoritmos = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}


# Normaliza (maiúsculo, sem espaços) e confere se a porta existe.
# Se não existir, devolve 404 "Porta não encontrada", como o professor pediu.
def validar_porta(porta):
    porta = porta.strip().upper()

    if porta not in grafo:
        raise HTTPException(status_code=404, detail="Porta não encontrada.")

    return porta


# Roda o algoritmo escolhido e monta a resposta no formato pedido.
def calcular_rota(nome_algoritmo, origem, destino):
    caminho, custo, visitados = algoritmos[nome_algoritmo](
        grafo, origem, destino
    )

    if not caminho:
        raise HTTPException(
            status_code=404,
            detail="Não existe caminho entre as portas.",
        )

    return {
        "algoritmo": nome_algoritmo,
        "caminho": caminho,
        "custo": custo,
        "unidade": "metros",
        "visitados": visitados,
    }


# GET /portas: devolve todas as portas em ordem alfabética.
@app.get("/portas", summary="Lista todas as portas", description="Devolve todas as portas do prédio em ordem alfabética.")
def listar_portas():
    return sorted(grafo.keys())


# GET /vizinhos/{porta}: devolve os vizinhos e o peso de cada aresta.
@app.get("/vizinhos/{porta}", summary="Lista os vizinhos de uma porta", description="Devolve as portas vizinhas e o peso (distância em metros) de cada ligação.")
def listar_vizinhos(porta: str):
    porta = validar_porta(porta)

    return [
        {"porta": vizinho, "peso": peso}
        for vizinho, peso in grafo[porta]
    ]


# GET /rota?origem=&destino=&algoritmo=: calcula uma rota.
@app.get("/rota", summary="Calcula uma rota", description="Calcula o caminho entre duas portas usando o algoritmo escolhido e devolve caminho, custo e visitados.")
def buscar_rota(
    origem: str,
    destino: str,
    algoritmo: str = Query(
        ...,
        pattern="^(bfs|dfs|gulosa|dijkstra)$",
        description="Algoritmo de busca: bfs, dfs, gulosa ou dijkstra.",
    ),
):
    origem = validar_porta(origem)
    destino = validar_porta(destino)

    return calcular_rota(algoritmo, origem, destino)


# GET /comparar?origem=&destino=: mostra os quatro algoritmos lado a lado.
@app.get("/comparar", summary="Compara os quatro algoritmos", description="Executa BFS, DFS, busca gulosa e Dijkstra entre duas portas e mostra os quatro resultados lado a lado.")
def comparar_algoritmos(origem: str, destino: str):
    origem = validar_porta(origem)
    destino = validar_porta(destino)

    return {
        nome: calcular_rota(nome, origem, destino)
        for nome in algoritmos
    }
