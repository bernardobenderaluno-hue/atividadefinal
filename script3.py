import math

# Constantes globais do veículo
CONSUMO_POR_KM = 0.35  # L/km
CAPACIDADE_TANQUE = 80.0  # L
ORIGEM = (0.0, 0.0)


def calcular_distancia(p1, p2):
    """Calcula a distância Euclidiana entre dois pontos."""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


# (a) Cálculo da rota original
def calcular_rota_original(pontos):
    distancia_total = 0.0
    ponto_atual = ORIGEM

    for ponto in pontos:
        distancia_total += calcular_distancia(ponto_atual, ponto)
        ponto_atual = ponto

    distancia_total += calcular_distancia(ponto_atual, ORIGEM)  # Retorno
    return distancia_total


# (b) Algoritmo do Vizinho Mais Próximo
def otimizar_rota_vizinho_mais_proximo(pontos):
    nao_visitados = pontos.copy()
    nova_ordem = []
    distancia_total = 0.0
    ponto_atual = ORIGEM

    while nao_visitados:
        # Encontra o ponto não visitado mais próximo
        mais_proximo = min(nao_visitados, key=lambda p: calcular_distancia(ponto_atual, p))
        distancia_total += calcular_distancia(ponto_atual, mais_proximo)

        nova_ordem.append(mais_proximo)
        nao_visitados.remove(mais_proximo)
        ponto_atual = mais_proximo

    distancia_total += calcular_distancia(ponto_atual, ORIGEM)  # Retorno
    return nova_ordem, distancia_total


# (c) Comparação de consumo
def comparar_consumo(dist_original, dist_otimizada):
    consumo_original = dist_original * CONSUMO_POR_KM
    consumo_otimizado = dist_otimizada * CONSUMO_POR_KM
    economia = consumo_original - consumo_otimizado

    return consumo_original, consumo_otimizado, economia


# (d) Verificação de abastecimento
def precisa_reabastecer(consumo_total):
    return consumo_total > CAPACIDADE_TANQUE


# Orquestrador Principal
def main():
    # Coordenadas de teste
    pontos_entrega = [(10, 20), (50, 50), (15, 5), (40, 10), (5, 60)]

    dist_orig = calcular_rota_original(pontos_entrega)
    rota_otim, dist_otim = otimizar_rota_vizinho_mais_proximo(pontos_entrega)

    cons_orig, cons_otim, economia = comparar_consumo(dist_orig, dist_otim)
    abastecimento_necessario = precisa_reabastecer(cons_otim)

    print("=== RELATÓRIO DE ROTAS ===")
    print(f"Distância Original: {dist_orig:.2f} km | Consumo: {cons_orig:.2f} L")
    print(f"Distância Otimizada: {dist_otim:.2f} km | Consumo: {cons_otim:.2f} L")
    print(f"Economia de Combustível: {economia:.2f} L")
    print(f"Nova ordem de visita: {rota_otim}")
    print(f"Reabastecimento na rota otimizada? {'SIM' if abastecimento_necessario else 'NÃO'}")


if __name__ == "__main__":
    main()