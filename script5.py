import matplotlib.pyplot as plt
import numpy as np

# =====================================================================
# 1. ENTRADA DE DADOS (Simulação de um cenário real de engenharia)
# =====================================================================
POTENCIA_SISTEMA_KWP = 85.0  # Potência do arranjo de painéis (kWp)
EFICIENCIA_GLOBAL = 0.80  # 80% (Perdas estimadas do sistema)
CUSTO_POR_KWP = 3800.0  # Custo de instalação por kWp (R$)
TARIFA_ENERGIA = 0.75  # Preço do kWh cobrado pela distribuidora (R$)
TAXA_DESCONTO_ANUAL = 0.10  # Taxa de atratividade financeira (10% a.a.)
VIDA_UTIL_ANOS = 25
DEGRADACAO_PAINEL = 0.005  # 0.5% de perda de eficiência por ano

# Vetores de 12 posições representando os meses do ano (Janeiro a Dezembro)
DIAS_MESES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
CONSUMO_MENSAL_KWH = [14200, 13800, 14500, 12900, 11500, 10800, 11200, 12000, 13100, 14000, 14300, 15000]
IRRADIANCIA_DIARIA_HSP = [6.2, 5.8, 5.1, 4.5, 3.8, 3.2, 3.5, 4.2, 4.8, 5.5, 6.0, 6.5]
MESES_NOMES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


# =====================================================================
# 2. PROCESSAMENTO TÉCNICO-ECONÔMICO
# =====================================================================

def simular_geracao_mensal():
    geracao_anual_base = []
    for hsp, dias in zip(IRRADIANCIA_DIARIA_HSP, DIAS_MESES):
        # E_gen = P_dc * HSP * Dias * Eficiência
        gen_mes = POTENCIA_SISTEMA_KWP * hsp * dias * EFICIENCIA_GLOBAL
        geracao_anual_base.append(gen_mes)
    return geracao_anual_base


class Fator_degradacao:
    pass


def calcular_viabilidade(geracao_mensal_base):
    investimento_inicial = POTENCIA_SISTEMA_KWP * CUSTO_POR_KWP
    geracao_total_ano_1 = sum(geracao_mensal_base)
    economia_ano_1 = geracao_total_ano_1 * TARIFA_ENERGIA

    fluxo_caixa_acumulado = [-investimento_inicial]
    lucro_anual = []
    vpl = -investimento_inicial
    payback_ano = -1

    # Simulação dos 25 anos considerando degradação do painel e valor do dinheiro no tempo
    for ano in range(1, VIDA_UTIL_ANOS + 1):
        # Rendimento decai a cada ano devido à degradação física
        fator_degradacao = (1 - DEGRADACAO_PAINEL) ** (ano - 1)
        ganho_ano = economia_ano_1 * Fator_degradacao
        lucro_anual.append(ganho_ano)

        # Atualização do Fluxo de Caixa Nominal Acumulado (para achar o payback simples)
        saldo_atual = fluxo_caixa_acumulado[-1] + ganho_ano
        fluxo_caixa_acumulado.append(saldo_atual)

        # Cálculo do VPL (Trazendo o ganho futuro para o valor presente)
        vpl += ganho_ano / ((1 + TAXA_DESCONTO_ANUAL) ** ano)

        # Detectar o ano de virada do fluxo de caixa (Payback)
        if saldo_atual >= 0 and payback_ano == -1:
            payback_ano = ano

    return investimento_inicial, fluxo_caixa_acumulado, vpl, payback_ano


# Execução das funções de cálculo
geracao_mensal = simular_geracao_mensal()
investimento, fluxo_acumulado, vpl_final, tempo_payback = calcular_viabilidade(geracao_mensal)

# =====================================================================
# 3. APRESENTAÇÃO DE RESULTADOS (TABELA NO TERMINAL)
# =====================================================================
print("=" * 70)
print(f"      BALANÇO ENERGÉTICO MENSAL - CAPACIDADE: {POTENCIA_SISTEMA_KWP} kWp")
print("=" * 70)
print(f"{'Mês':<6} | {'Consumo (kWh)':<14} | {'Geração (kWh)':<14} | {'Balanço Líquido (kWh)':<20}")
print("-" * 70)
for i in range(12):
    balanco = geracao_mensal[i] - CONSUMO_MENSAL_KWH[i]
    print(f"{MESES_NOMES[i]:<6} | {CONSUMO_MENSAL_KWH[i]:<14.1f} | {geracao_mensal[i]:<14.1f} | {balanco:<+20.1f}")
print("=" * 70)
print(f"Investimento Inicial: R$ {investimento:,.2f}")
print(f"Retorno do Investimento (Payback Simples): {tempo_payback} anos")
print(f"Valor Presente Líquido (VPL após 25 anos): R$ {vpl_final:,.2f} (Taxa: {TAXA_DESCONTO_ANUAL * 100}%)")
print("=" * 70)

# =====================================================================
# 4. REPRESENTAÇÕES VISUAIS (GRÁFICOS)
# =====================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Gráfico 1: Comparativo Mensal de Energia
x = np.arange(len(MESES_NOMES))
largura = 0.35

ax1.bar(x - largura / 2, CONSUMO_MENSAL_KWH, largura, label='Consumo da Fábrica', color='#e74c3c')
ax1.bar(x + largura / 2, geracao_mensal, largura, label='Geração Estimada Solar', color='#f1c40f')
ax1.set_title('Perfil de Consumo Elétrico vs. Geração Fotovoltaica')
ax1.set_xlabel('Meses do Ano')
ax1.set_ylabel('Energia (kWh)')
ax1.set_xticks(x)
ax1.set_xticklabels(MESES_NOMES)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.legend()

# Gráfico 2: Curva de Payback e Fluxo de Caixa Acumulado
anos_eixo = list(range(0, VIDA_UTIL_ANOS + 1))
ax2.plot(anos_eixo, fluxo_acumulado, marker='o', color='#2ecc71', linewidth=2, label='Saldo Acumulado')
ax2.axhline(0, color='black', linestyle='-', linewidth=1)
ax2.axvline(tempo_payback, color='#9b59b6', linestyle='--', label=f'Ponto de Payback ({tempo_payback} anos)')
ax2.fill_between(anos_eixo, fluxo_acumulado, 0, where=(np.array(fluxo_acumulado) >= 0), color='#2ecc71', alpha=0.2)
ax2.fill_between(anos_eixo, fluxo_acumulado, 0, where=(np.array(fluxo_acumulado) < 0), color='#e74c3c', alpha=0.2)
ax2.set_title('Curva de Retorno Financeiro ao Longo de 25 Anos')
ax2.set_xlabel('Tempo de Operação (Anos)')
ax2.set_ylabel('Capital Acumulado (R$)')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.show()