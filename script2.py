import json
import os
from datetime import datetime

# ==========================================
# CONFIGURAÇÕES E DADOS DE ENTRADA (MOCK/MÁRTIRES)
# ==========================================
# Simulando a captura de dados brutos de portais locais sobre o esporte alegretense
DADOS_BRUTOS_EVENTOS = [
    {
        "nome": "45º EFIPAN - Encontro de Futebol Infantil Pan-Americano",
        "modalidade": "Futebol de Campo Sub-14",
        "data": "18/01/2026",
        "local": "Estádio Farroupilha",
        "link_oficial": "https://www.efipan.com.br",
        "redes_sociais": {"instagram": "@efipan_oficial"},
        "historico": "Maior torneio infantil da América Latina, revelou Ronaldinho e Neymar."
    },
    {
        "nome": "Campeonato Citadino de Futsal de Alegrete",
        "modalidade": "Futsal",
        "data": "12/10/2026",
        "local": "Ginásio Municipal Oswaldo Aranha",
        "link_oficial": "N/A",
        "redes_sociais": {"facebook": "Futsal Alegretense"},
        "historico": "Edições anuais com ampla participação dos bairros da cidade."
    },
    {
        "nome": "Rústica Noturna de Aniversário de Alegrete",
        "modalidade": "Corrida de Rua / Atletismo",
        "data": "24/10/2026",
        "local": "Largada na Praça Getúlio Vargas",
        "link_oficial": "https://alegrete.rs.gov.br/eventos",
        "redes_sociais": {},
        "historico": "Comemoração do aniversário do município."
    },
    {
        "nome": "Torneio Inválido de Teste",
        "modalidade": "Desconhecida",
        "data": "data_corrompida",  # Simulação de erro para testar a validação
        "local": "",
        "link_oficial": "",
        "redes_sociais": {},
        "historico": ""
    }
]


# ==========================================
# FUNÇÕES MODULARES (RESPONSABILIDADE ÚNICA)
# ==========================================

def validar_evento(evento: dict) -> bool:
    """Valida se o evento possui os campos mínimos obrigatórios e data correta."""
    if not evento.get("nome") or not evento.get("modalidade") or not evento.get("local"):
        return False

    # Validação do formato da data (DD/MM/AAAA)
    try:
        datetime.strptime(evento["data"], "%d/%m/%Y")
        return True
    except ValueError:
        return False  # Descarta se a data for inválida ou texto corrompido


def processar_catalogo(lista_bruta: list) -> tuple:
    """Separa os eventos entre válidos e descartados."""
    validos = []
    descartados = 0

    for item in lista_bruta:
        if validar_evento(item):
            validos.append(item)
        else:
            descartados += 1

    return validos, descartados


def exportar_para_json(dados: list, nome_arquivo: str = "catalogo_esportes_alegrete.json") -> bool:
    """Salva a lista de eventos validados em um arquivo JSON estruturado."""
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"[Erro] Falha ao salvar o arquivo: {e}")
        return False


def exibir_relatorio_terminal(validos: list, descartados: int):
    """Gera o output formatado para o usuário no terminal (Visualização rápida)."""
    print("=" * 60)
    print("      PORTAL ALEGRETE.ORG - SISTEMA DE GESTÃO ESPORTIVA      ")
    print("=" * 60)
    print(f"Total de Eventos Processados com Sucesso: {len(validos)}")
    print(f"Total de Registros Descartados (Erros/Incompletos): {descartados}")
    print("-" * 60)

    for i, ev in enumerate(validos, start=1):
        print(f"{i}. {ev['nome'].upper()}")
        print(f"   • Modalidade: {ev['modalidade']}")
        print(f"   • Data Prevista: {ev['data']} | Local: {ev['local']}")
        print(f"   • Redes/Links: {ev['link_oficial']} | {ev['redes_sociais']}")
        print(f"   • Histórico: {ev['historico']}")
        print("-" * 60)


# ==========================================
# FLUXO PRINCIPAL (ORQUESTRAÇÃO)
# ==========================================

def main():
    # 1. Processamento e Validação
    eventos_validos, qtd_descartados = processar_catalogo(DADOS_BRUTOS_EVENTOS)

    # 2. Persistência dos Dados (Geração do artefato para o site)
    sucesso_salvamento = exportar_para_json(eventos_validos)

    # 3. Output de Feedback
    if sucesso_salvamento:
        print(f"[Sucesso] Arquivo 'catalogo_esportes_alegrete.json' gerado!")

    exibir_relatorio_terminal(eventos_validos, qtd_descartados)


if __name__ == "__main__":
    main()