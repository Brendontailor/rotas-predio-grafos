# Carrega as arestas e monta a lista de adjacência.
# Este módulo é responsável por ler o arquivo de arestas (arestas.txt) e construir
# a representação do grafo como uma lista de adjacência bidirecional.

def carregar_grafo(caminho):
    """
    Carrega um grafo a partir de um arquivo de texto contendo arestas.
    
    Args:
        caminho (str): Caminho para o arquivo de arestas.
        
    Returns:
        dict: Dicionário representando o grafo como lista de adjacência.
              Chaves são nomes dos vértices (portas), valores são listas de tuplas
              (vizinho, peso).
              
    Raises:
        ValueError: Se o formato do arquivo for inválido (linha com número errado
                    de partes, peso não numérico, ou peso <= 0).
        FileNotFoundError: Se o arquivo não existir.
    """
    grafo = {}

    # Abre o arquivo com codificação UTF-8 para suportar caracteres especiais
    with open(caminho, "r", encoding="utf-8") as arquivo:
        # Enumera linhas começando em 1 para mensagens de erro claras
        for numero_linha, linha in enumerate(arquivo, start=1):
            # Remove espaços em branco no início e fim da linha
            linha = linha.strip()

            # Ignora linhas vazias e comentários (linhas que começam com #)
            if not linha or linha.startswith("#"):
                continue

            # Divide a linha em partes separadas por whitespace
            # Espera-se exatamente 3 partes: origem, destino, peso
            partes = linha.split()
            if len(partes) != 3:
                raise ValueError(f"Linha {numero_linha} inválida.")

            origem, destino, peso_texto = partes

            # Converte o peso para float, com tratamento de erro
            try:
                peso = float(peso_texto)
            except ValueError as erro:
                raise ValueError(
                    f"Peso inválido na linha {numero_linha}."
                ) from erro

            # Valida que o peso é positivo (distâncias não podem ser zero ou negativas)
            if peso <= 0:
                raise ValueError(f"O peso deve ser positivo na linha {numero_linha}.")

            # Adiciona a aresta nos dois sentidos (grafo não direcionado)
            # setdefault cria a lista se a chave não existir, depois adiciona a tupla
            grafo.setdefault(origem, []).append((destino, peso))
            grafo.setdefault(destino, []).append((origem, peso))

    return grafo
