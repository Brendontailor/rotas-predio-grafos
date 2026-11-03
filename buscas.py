#- Implementa algoritmos de busca em grafos: BFS, DFS, Gulosa e Dijkstra.
# Cada algoritmo tem características diferentes:
# - BFS: encontra caminho com MENOR NÚMERO DE ARESTAS (não considera pesos)
# - DFS: explora o mais profundo possível antes de voltar (não garante optimalidade)
# - Gulosa: sempre escolhe a aresta de menor peso IMEDIATO (pode não ser ótima globalmente)
# - Dijkstra: encontra o caminho de MENOR CUSTO TOTAL (soma dos pesos) - ÓTIMO para pesos positivos

import heapq       # Heap (fila de prioridade) para Dijkstra e Gulosa - O(log n) para inserção/remoção
from collections import deque  # Fila de duas pontas (double-ended queue) para BFS - O(1) popleft()


def calcular_custo(grafo, caminho):
    """
    Calcula o custo total de um caminho somando os pesos das arestas percorridas.
    
    Args:
        grafo (dict): Grafo como lista de adjacência {vertice: [(vizinho, peso), ...]}
        caminho (list): Lista de vértices representando o caminho [origem, ..., destino]
        
    Returns:
        float: Custo total arredondado com 2 casas decimais
        
    Exemplo:
        caminho = ["A", "B", "C"] com arestas A-B=5, B-C=3
        retorna 8.0
    """
    custo = 0

    # Percorre o caminho de dois em dois vértices consecutivos
    for indice in range(len(caminho) - 1):
        atual = caminho[indice]
        proxima = caminho[indice + 1]

        # Procura a aresta entre 'atual' e 'proxima' na lista de adjacência
        for vizinho, peso in grafo[atual]:
            if vizinho == proxima:
                custo += peso
                break

    return round(custo, 2)


def reconstruir_caminho(anterior, origem, destino):
    """
    Reconstrói o caminho percorrido a partir do dicionário 'anterior'.
    
    Durante as buscas, guardamos para cada vértice visitado qual foi o vértice
    anterior (de onde viemos). Para reconstruir o caminho completo, começamos
    no destino e voltamos seguindo os 'anteriores' até chegar na origem.
    
    Args:
        anterior (dict): Dicionário {vertice: vertice_anterior} preenchido durante a busca
        origem (str): Vértice de início do caminho
        destino (str): Vértice final do caminho
        
    Returns:
        list: Lista de vértices do caminho [origem, ..., destino] ou [] se não houver caminho
        
    Exemplo:
        anterior = {"A": None, "B": "A", "C": "B"}  # A -> B -> C
        reconstruir_caminho(anterior, "A", "C") retorna ["A", "B", "C"]
    """
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anterior.get(atual)

    caminho.reverse()

    if not caminho or caminho[0] != origem:
        return []

    return caminho


def bfs(grafo, origem, destino):
    """
    Busca em Largura (Breadth-First Search) - BFS
    
    Explora o grafo camada por camada: primeiro todos os vizinhos da origem,
    depois os vizinhos dos vizinhos, e assim por diante.
    
    Características:
    - Usa uma FILA (FIFO - First In, First Out)
    - Garante encontrar o caminho com MENOR NÚMERO DE ARESTAS
    - NÃO considera os pesos das arestas durante a busca
    - Completo: sempre encontra um caminho se existir (em grafos finitos)
    - Complexidade: O(V + E) onde V=vértices, E=arestas
    
    Args:
        grafo (dict): Grafo como lista de adjacência
        origem (str): Vértice inicial
        destino (str): Vértice final desejado
        
    Returns:
        tuple: (caminho, custo, visitados)
            - caminho (list): Lista de vértices [origem, ..., destino] ou [] se não achar
            - custo (float): Soma dos pesos do caminho encontrado (inf se não achar)
            - visitados (int): Quantidade de vértices visitados durante a busca
    """
    if origem not in grafo or destino not in grafo:
        return [], float("inf"), 0

    fila = deque([origem])
    anterior = {origem: None}
    visitados = 0

    while fila:
        atual = fila.popleft()
        visitados += 1

        if atual == destino:
            caminho = reconstruir_caminho(anterior, origem, destino)
            return caminho, calcular_custo(grafo, caminho), visitados

        for vizinho, _ in grafo[atual]:
            if vizinho not in anterior:
                anterior[vizinho] = atual
                fila.append(vizinho)

    return [], float("inf"), visitados


def dfs(grafo, origem, destino):
    """
    Busca em Profundidade (Depth-First Search) - DFS
    
    Explora o máximo possível em cada ramificação antes de voltar (backtracking).
    Vai "fundo" no grafo antes de explorar irmãos.
    
    Características:
    - Usa uma PILHA (LIFO - Last In, First Out)
    - NÃO garante caminho ótimo (nem em arestas, nem em pesos)
    - Útil para: detectar ciclos, ordenação topológica, labirintos
    - Complexidade: O(V + E)
    
    Args:
        grafo (dict): Grafo como lista de adjacência
        origem (str): Vértice inicial
        destino (str): Vértice final desejado
        
    Returns:
        tuple: (caminho, custo, visitados)
    """
    if origem not in grafo or destino not in grafo:
        return [], float("inf"), 0

    pilha = [origem]
    anterior = {origem: None}
    visitados_set = set()
    visitados = 0

    while pilha:
        atual = pilha.pop()

        if atual in visitados_set:
            continue

        visitados_set.add(atual)
        visitados += 1

        if atual == destino:
            caminho = reconstruir_caminho(anterior, origem, destino)
            return caminho, calcular_custo(grafo, caminho), visitados

        for vizinho, _ in reversed(grafo[atual]):
            if vizinho not in visitados_set and vizinho not in anterior:
                anterior[vizinho] = atual
                pilha.append(vizinho)

    return [], float("inf"), visitados


def gulosa(grafo, origem, destino):
    """
    Busca Gulosa (Greedy Best-First Search)
    
    Sempre expande o vértice que PARECE mais promissor no momento:
    escolhe o vizinho com MENOR PESO IMEDIATO (menor aresta saindo do atual).
    
    Características:
    - Usa FILA DE PRIORIDADE (heap) ordenada pelo PESO DA ARESTA IMEDIATA
    - NÃO garante optimalidade global
    - Mais rápida que Dijkstra em muitos casos, mas pode dar resultado subótimo
    - Complexidade: O(E log V) com heap
    
    Diferença para Dijkstra:
    - Gulosa: prioridade = peso da aresta ATUAL -> vizinho (custo local)
    - Dijkstra: prioridade = custo TOTAL acumulado da origem até o vizinho (custo global)
    
    Args:
        grafo (dict): Grafo como lista de adjacência
        origem (str): Vértice inicial
        destino (str): Vértice final desejado
        
    Returns:
        tuple: (caminho, custo, visitados)
    """
    if origem not in grafo or destino not in grafo:
        return [], float("inf"), 0

    fila = []
    ordem = 0
    heapq.heappush(fila, (0, ordem, origem))
    
    anterior = {origem: None}
    finalizadas = set()

    while fila:
        _, _, atual = heapq.heappop(fila)

        if atual in finalizadas:
            continue

        finalizadas.add(atual)

        if atual == destino:
            caminho = reconstruir_caminho(anterior, origem, destino)
            return caminho, calcular_custo(grafo, caminho), len(finalizadas)

        for vizinho, peso in grafo[atual]:
            if vizinho not in finalizadas and vizinho not in anterior:
                anterior[vizinho] = atual
                ordem += 1
                heapq.heappush(fila, (peso, ordem, vizinho))

    return [], float("inf"), len(finalizadas)


def dijkstra(grafo, origem, destino):
    """
    Algoritmo de Dijkstra - Caminho de menor custo em grafos com pesos POSITIVOS
    
    Encontra o caminho de MENOR CUSTO TOTAL (soma dos pesos) da origem ao destino.
    É ótimo e completo para grafos com pesos não-negativos.
    
    Características:
    - Usa FILA DE PRIORIDADE (min-heap) ordenada pelo CUSTO ACUMULADO
    - Mantém tabela 'distancia' com menor custo conhecido da origem a cada vértice
    - Quando um vértice é removido da fila (finalizado), seu custo é DEFINITIVO
    - Complexidade: O(E log V) com heap binário
    
    Args:
        grafo (dict): Grafo como lista de adjacência {v: [(vizinho, peso), ...]}
        origem (str): Vértice inicial
        destino (str): Vértice final desejado
        
    Returns:
        tuple: (caminho, custo, visitados)
            - caminho: lista de vértices [origem, ..., destino]
            - custo: menor custo total (float)
            - visitados: nº de vértices finalizados
    """
    if origem not in grafo or destino not in grafo:
        return [], float("inf"), 0

    distancia = {porta: float("inf") for porta in grafo}
    anterior = {origem: None}
    distancia[origem] = 0

    fila = [(0, origem)]
    finalizadas = set()

    while fila:
        custo_atual, atual = heapq.heappop(fila)

        if atual in finalizadas:
            continue

        finalizadas.add(atual)

        if atual == destino:
            caminho = reconstruir_caminho(anterior, origem, destino)
            return caminho, round(distancia[destino], 2), len(finalizadas)

        for vizinho, peso in grafo[atual]:
            novo_custo = custo_atual + peso

            if novo_custo < distancia[vizinho]:
                distancia[vizinho] = novo_custo
                anterior[vizinho] = atual
                heapq.heappush(fila, (novo_custo, vizinho))

    return [], float("inf"), len(finalizadas)