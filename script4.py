import matplotlib.pyplot as plt


# ==========================================
# CONFIGURAÇÕES E ENTRADA DINÂMICA DE DADOS
# ==========================================

def obter_dados_trelica():
    """Solicita os dados das barras dinamicamente do usuário."""
    print("=== CONFIGURAÇÃO DA TRELIÇA PLANAS ===")

    # Propriedades do Material (Exemplo: Aço ASTM A36)
    while True:
        try:
            tensao_adm = float(input("Digite a tensão admissível do material (MPa) [Ex: 250]: "))
            break
        except ValueError:
            print("Por favor, insira um valor numérico válido.")

    while True:
        try:
            num_elementos = int(input("Quantas barras/elementos possui a treliça?: "))
            if num_elementos > 0:
                break
            print("A quantidade de elementos deve ser maior que zero.")
        except ValueError:
            print("Por favor, insira um número inteiro.")

    forcas = []  # Vetor dinâmico para forças axiais (kN)
    areas = []  # Vetor dinâmico para áreas de seção transversal (cm²)
    identificadores = []  # Nomes das barras (ex: Barra 1, Barra 2...)

    print("\n--- Entrada de Dados por Elemento ---")
    print("Nota: Use valores POSITIVOS para Tração e NEGATIVOS para Compressão.")

    for i in range(num_elementos):
        id_barra = f"Barra {i + 1}"
        identificadores.append(id_barra)

        while True:
            try:
                f = float(input(f"[{id_barra}] Força axial atuante (kN): "))
                a = float(input(f"[{id_barra}] Área da seção transversal (cm²): "))
                if a <= 0:
                    print("A área deve ser estritamente positiva.")
                    continue
                forcas.append(f)
                areas.append(a)
                break
            except ValueError:
                print("Entrada inválida. Digite números reais.")

    return tensao_adm, num_elementos, identificadores, forcas, areas


# ==========================================
# PROCESSAMENTO MATEMÁTICO E REGRAS DE NEGÓCIO
# ==========================================

def calcular_tensoes_e_seguranca(forcas, areas, tensao_adm):
    """Calcula tensões em MPa, classifica esforços e gera fatores de segurança."""
    tensoes = []
    classificacoes = []
    fatores_seguranca = []

    for f, a in zip(forcas, areas):
        # Conversão de unidades: (kN / cm²) * 10 = MPa
        tensao = (f / a) * 10
        tensoes.append(tensao)

        # Classificação do esforço
        if tensao > 0:
            classificacoes.append("Tração")
        elif tensao < 0:
            classificacoes.append("Compressão")
        else:
            classificacoes.append("Nulo")

        # Cálculo do Fator de Segurança (FS)
        if tensao != 0:
            fs = tensao_adm / abs(tensao)
            fatores_seguranca.append(round(fs, 2))
        else:
            fatores_seguranca.append(float('inf'))  # Elemento de força zero

    return tensoes, classificacoes, fatores_seguranca


# ==========================================
# OUTPUTS: TABELAS E GRÁFICOS VISUAIS
# ==========================================

def exibir_tabela_resultados(ids, forcas, areas, tensoes, classes, fatores, tensao_adm):
    """Formata e exibe os resultados estruturais no terminal."""
    print("\n" + "=" * 85)
    print(f"               RELATÓRIO TÉCNICO: ANÁLISE DE TENSÕES (σ_adm = {tensao_adm} MPa)               ")
    print("=" * 85)
    header = f"{'Elemento':<12} | {'Força (kN)':<12} | {'Área (cm²)':<12} | {'Tensão (MPa)':<14} | {'Esforço':<12} | {'F.S.':<8}"
    print(header)
    print("-" * 85)

    for i in range(len(ids)):
        # Alerta visual se o Fator de Segurança for menor que 1 (Estrutura falha)
        status_fs = f"{fatores[i]:.2f}" if fatores[i] != float('inf') else "INF"
        if fatores[i] < 1.0:
            status_fs += " ❌ (FALHA)"

        row = f"{ids[i]:<12} | {forcas[i]:<12.2f} | {areas[i]:<12.2f} | {tensoes[i]:<14.2f} | {classes[i]:<12} | {status_fs:<8}"
        print(row)
    print("=" * 85 + "\n")


def plotar_graficos_trelica(ids, tensoes, forcas, tensao_adm):
    """Gera visualizações gráficas das tensões e carregamentos."""
    # Criando uma figura com 2 subplots (lado a lado)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico 1: Tensões vs Limite Admissível
    cores_tensoes = ['#2ca02c' if abs(sigma) <= tensao_adm else '#d62728' for sigma in tensoes]
    ax1.bar(ids, [abs(sigma) for sigma in tensoes], color=cores_tensoes, alpha=0.8, edgecolor='black')
    ax1.axhline(y=tensao_adm, color='red', linestyle='--', linewidth=2, label=f'Tensão Admissível ({tensao_adm} MPa)')
    ax1.set_title("Magnitude da Tensão Absoluta por Elemento")
    ax1.set_xlabel("Barras da Treliça")
    ax1.set_ylabel("|σ| (MPa)")
    ax1.grid(axis='y', linestyle=':', alpha=0.6)
    ax1.legend()

    # Gráfico 2: Perfil de Forças Axiais (Sinalizado)
    cores_forcas = ['#1f77b4' if f >= 0 else '#ff7f0e' for f in forcas]
    ax2.bar(ids, forcas, color=cores_forcas, edgecolor='black')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_title("Diagrama de Forças Axiais Atuantes")
    ax2.set_xlabel("Barras da Treliça")
    ax2.set_ylabel("Força Axial (kN)")
    # Customização de legenda manual para tração/compressão
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#1f77b4', label='Tração (+)'),
                       Patch(facecolor='#ff7f0e', label='Compressão (-)')]
    ax2.legend(handles=legend_elements)
    ax2.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.show()


# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================

def main():
    # 1. Coleta de dados dinâmicos
    t_adm, _, barras, forcas, areas = obter_dados_trelica()

    # 2. Processamento dos vetores
    tensoes, classes, fatores = calcular_tensoes_e_seguranca(forcas, areas, t_adm)

    # 3. Retorno dos resultados
    exibir_tabela_resultados(barras, forcas, areas, tensoes, classes, fatores, t_adm)
    plotar_graficos_trelica(barras, tensoes, forcas, t_adm)


if __name__ == "__main__":
    main()
