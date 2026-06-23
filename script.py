import statistics


def validar_dados(dados_brutos):
    validos = []
    descartados = 0
    for item in dados_brutos:
        try:
            valor = float(item)
            if -120 <= valor <= 0:
                validos.append(valor)
            else:
                descartados += 1
        except (ValueError, TypeError):
            descartados += 1
    return validos, descartados


def calcular_estatisticas(validos, descartados):
    if not validos:
        return None
    return {
        "media": statistics.mean(validos),
        "minimo": min(validos),
        "maximo": max(validos),
        "desvio_padrao": statistics.stdev(validos) if len(validos) > 1 else 0.0,
        "qtd_validas": len(validos),
        "qtd_descartadas": descartados
    }


def classificar_medicoes(validos):
    classificacoes = []
    for v in validos:
        if v < -100:
            classificacoes.append((v, "Crítico"))
        elif v < -85:
            classificacoes.append((v, "Alerta"))
        else:
            classificacoes.append((v, "Normal"))
    return classificacoes


def detectar_eventos(validos):
    total_criticos = 0
    maior_seq = 0
    seq_atual = 0

    for v in validos:
        if v < -100:
            total_criticos += 1
            seq_atual += 1
            if seq_atual > maior_seq:
                maior_seq = seq_atual
        else:
            seq_atual = 0

    return total_criticos, maior_seq


def gerar_relatorio(stats, classificacoes, eventos):
    print("=" * 40)
    print(" RELATÓRIO DE MONITORAMENTO - TELECOM ")
    print("=" * 40)
    if not stats:
        print("Nenhum dado válido para analisar.")
        return

    print(f"Amostras Válidas: {stats['qtd_validas']}")
    print(f"Amostras Descartadas: {stats['qtd_descartadas']}")
    print(f"Média: {stats['media']:.2f} dBm")
    print(f"Mínimo: {stats['minimo']:.2f} dBm")
    print(f"Máximo: {stats['maximo']:.2f} dBm")
    print(f"Desvio Padrão: {stats['desvio_padrao']:.2f} dBm")
    print("-" * 40)
    print(f"Total de medições críticas: {eventos[0]}")
    print(f"Maior sequência crítica: {eventos[1]}")
    print("=" * 40)


def main():
    dados_brutos = [-90, -105, -110, "erro", -50, -125, -95, -102, -101, -40]
    validos, descartados = validar_dados(dados_brutos)
    stats = calcular_estatisticas(validos, descartados)
    classificacoes = classificar_medicoes(validos)
    eventos = detectar_eventos(validos)
    gerar_relatorio(stats, classificacoes, eventos)


if __name__ == "__main__":
    main()

