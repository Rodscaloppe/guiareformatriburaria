"""Simulador Prático da Construção Civil na Reforma Tributária (LC 214/2025).

Implementa os 3 Exemplos Práticos completos envolvendo:
1. Incorporadora (Edifício Residencial com Redutor de Ajuste, Redutor Social e Créditos);
2. Construtora em Empreitada Global B2B + Empreiteira + Serviços Complementares;
3. Administradora de Obras (Obra por Administração vs. Empreitada Global para PF).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ParametrosConstrucao:
    """Alíquotas de referência para o setor de Construção Civil (LC 214/2025)."""

    aliquota_padrao: float = 0.265
    reducao_imobiliario: float = 0.50
    reducao_engenharia_arquitetura: float = 0.30
    redutor_social_apto: float = 100_000.00

    @property
    def aliq_construcao(self) -> float:
        """Alíquota com redução de 50% (13,25% para padrão de 26,5%)."""
        return round(self.aliquota_padrao * (1.0 - self.reducao_imobiliario), 6)

    @property
    def aliq_especialistas_projetos(self) -> float:
        """Alíquota com redução de 30% (18,55% para padrão de 26,5%)."""
        return round(self.aliquota_padrao * (1.0 - self.reducao_engenharia_arquitetura), 6)


def simular_exemplo_1_incorporacao(
    qtd_apartamentos: int = 10,
    preco_unitario_apto: float = 500_000.00,
    custo_terreno: float = 1_000_000.00,
    custo_projetos_especialistas: float = 200_000.00,
    custo_servicos_complementares: float = 400_000.00,
    custo_materiais: float = 1_200_000.00,
    custo_empreiteira: float = 800_000.00,
    params: ParametrosConstrucao = ParametrosConstrucao(),
) -> dict:
    """Exemplo 1: Incorporação Residencial na Planta com os 5 elos da cadeia."""
    vgv_total = round(qtd_apartamentos * preco_unitario_apto, 2)
    redutor_social_total = round(qtd_apartamentos * params.redutor_social_apto, 2)
    base_calculo = max(0.0, round(vgv_total - custo_terreno - redutor_social_total, 2))
    debito_bruto = round(base_calculo * params.aliq_construcao, 2)

    cred_projetos = round(custo_projetos_especialistas * params.aliq_especialistas_projetos, 2)
    cred_complementares = round(custo_servicos_complementares * params.aliq_construcao, 2)
    cred_materiais = round(custo_materiais * params.aliquota_padrao, 2)
    cred_empreiteira = round(custo_empreiteira * params.aliq_construcao, 2)
    total_creditos = round(
        cred_projetos + cred_complementares + cred_materiais + cred_empreiteira, 2
    )

    diferenca = round(debito_bruto - total_creditos, 2)
    imposto_a_pagar = max(0.0, diferenca)
    saldo_credor = max(0.0, round(-diferenca, 2))
    carga_efetiva_cadeia_pct = round((debito_bruto / vgv_total) * 100, 2) if vgv_total > 0 else 0.0

    return {
        "vgv_total": vgv_total,
        "redutor_terreno": custo_terreno,
        "redutor_social_total": redutor_social_total,
        "base_calculo": base_calculo,
        "debito_bruto": debito_bruto,
        "cred_projetos": cred_projetos,
        "cred_complementares": cred_complementares,
        "cred_materiais": cred_materiais,
        "cred_empreiteira": cred_empreiteira,
        "total_creditos": total_creditos,
        "imposto_liquido_a_pagar": imposto_a_pagar,
        "saldo_credor": saldo_credor,
        "carga_efetiva_cadeia_pct": carga_efetiva_cadeia_pct,
    }


def simular_exemplo_2_empreitada_global_b2b(
    preco_obra_liquido: float = 2_000_000.00,
    custo_materiais: float = 900_000.00,
    custo_empreiteira: float = 400_000.00,
    custo_servicos_complementares: float = 200_000.00,
    params: ParametrosConstrucao = ParametrosConstrucao(),
) -> dict:
    """Exemplo 2: Construtora em Empreitada Global B2B (Galpão Industrial)."""
    cred_materiais = round(custo_materiais * params.aliquota_padrao, 2)
    cred_empreiteira = round(custo_empreiteira * params.aliq_construcao, 2)
    cred_complementares = round(custo_servicos_complementares * params.aliq_construcao, 2)
    total_creditos_construtora = round(
        cred_materiais + cred_empreiteira + cred_complementares, 2
    )

    debito_nf_construtora = round(preco_obra_liquido * params.aliq_construcao, 2)
    valor_total_nf = round(preco_obra_liquido + debito_nf_construtora, 2)

    diferenca = round(debito_nf_construtora - total_creditos_construtora, 2)
    imposto_liquido_construtora = max(0.0, diferenca)
    saldo_credor_construtora = max(0.0, round(-diferenca, 2))

    credito_industria_cliente = debito_nf_construtora
    custo_liquido_real_industria = round(valor_total_nf - credito_industria_cliente, 2)

    return {
        "preco_obra_liquido": preco_obra_liquido,
        "debito_nf_construtora": debito_nf_construtora,
        "valor_total_nf": valor_total_nf,
        "total_creditos_construtora": total_creditos_construtora,
        "imposto_liquido_construtora": imposto_liquido_construtora,
        "saldo_credor_construtora": saldo_credor_construtora,
        "credito_industria_cliente": credito_industria_cliente,
        "custo_liquido_real_industria": custo_liquido_real_industria,
    }


def simular_exemplo_3_administracao_vs_empreitada_pf(
    custo_projetos_especialistas: float = 100_000.00,
    custo_materiais: float = 500_000.00,
    custo_empreiteiras_complementares: float = 400_000.00,
    taxa_administracao: float = 120_000.00,
    params: ParametrosConstrucao = ParametrosConstrucao(),
) -> dict:
    """Exemplo 3: Administradora de Obras vs. Empreitada Global para Pessoa Física."""
    custo_total_liquido = round(
        custo_projetos_especialistas
        + custo_materiais
        + custo_empreiteiras_complementares
        + taxa_administracao,
        2,
    )

    imp_projetos = round(custo_projetos_especialistas * params.aliq_especialistas_projetos, 2)
    imp_materiais = round(custo_materiais * params.aliquota_padrao, 2)
    imp_empreiteiras = round(custo_empreiteiras_complementares * params.aliq_construcao, 2)
    imp_administradora = round(taxa_administracao * params.aliq_construcao, 2)

    imposto_total_administracao = round(
        imp_projetos + imp_materiais + imp_empreiteiras + imp_administradora, 2
    )
    custo_final_pf_administracao = round(custo_total_liquido + imposto_total_administracao, 2)

    imposto_total_empreitada_global = round(custo_total_liquido * params.aliq_construcao, 2)
    custo_final_pf_empreitada = round(custo_total_liquido + imposto_total_empreitada_global, 2)
    economia_empreitada_para_pf = round(
        custo_final_pf_administracao - custo_final_pf_empreitada, 2
    )

    return {
        "custo_total_liquido": custo_total_liquido,
        "imposto_administradora_sobre_taxa": imp_administradora,
        "imposto_total_modalidade_administracao": imposto_total_administracao,
        "custo_final_pf_administracao": custo_final_pf_administracao,
        "imposto_total_modalidade_empreitada": imposto_total_empreitada_global,
        "custo_final_pf_empreitada": custo_final_pf_empreitada,
        "economia_empreitada_para_pf": economia_empreitada_para_pf,
    }


def exibir_relatorio_construcao() -> None:
    """Imprime o resumo executivo dos 3 exemplos práticos da Construção Civil."""
    print("=" * 80)
    print("SIMULADOR SETORIAL: CONSTRUÇÃO CIVIL NA REFORMA TRIBUTÁRIA (LC 214/2025)")
    print("=" * 80)

    ex1 = simular_exemplo_1_incorporacao()
    print("\n[EXEMPLO 1] INCORPORADORA + ESPECIALISTAS + EMPREITEIRA (10 Aptos = R$ 5,0 Mi):")
    print(f"  Base de Cálculo (após Terreno e Redutor Social): R$ {ex1['base_calculo']:12.2f}")
    print(f"  (+) Débito Bruto da Incorporação (13,25%):       R$ {ex1['debito_bruto']:12.2f}")
    print(f"  (-) Créditos (Projetos+Compl.+Materiais+Empr.):  R$ {ex1['total_creditos']:12.2f}")
    print(f"  (=) Imposto Adicional a Pagar:                   R$ {ex1['imposto_liquido_a_pagar']:12.2f}")
    print(f"  (=) Saldo Credor Gerado para a Incorporadora:    R$ {ex1['saldo_credor']:12.2f}")

    ex2 = simular_exemplo_2_empreitada_global_b2b()
    print("\n[EXEMPLO 2] CONSTRUTORA (EMPREITADA GLOBAL B2B - GALPÃO DE R$ 2,0 Mi):")
    print(f"  Nota Fiscal da Construtora (R$ 2Mi + 13,25%):    R$ {ex2['valor_total_nf']:12.2f}")
    print(f"  Créditos da Construtora (Mat. 26,5% + Subempr.): R$ {ex2['total_creditos_construtora']:12.2f}")
    print(f"  Crédito Recuperado pela Indústria Cliente (B2B): R$ {ex2['credito_industria_cliente']:12.2f}")
    print(f"  Custo Líquido Final do Galpão para a Indústria:  R$ {ex2['custo_liquido_real_industria']:12.2f}")

    ex3 = simular_exemplo_3_administracao_vs_empreitada_pf()
    print("\n[EXEMPLO 3] ADMINISTRADORA DE OBRAS vs. EMPREITADA GLOBAL (CASA PF R$ 1,12 Mi):")
    print(f"  IBS/CBS da Administradora (13,25% s/ R$ 120mil): R$ {ex3['imposto_administradora_sobre_taxa']:12.2f}")
    print(f"  Custo Total p/ PF na Obra por Administração:     R$ {ex3['custo_final_pf_administracao']:12.2f}")
    print(f"  Custo Total p/ PF na Empreitada Global:          R$ {ex3['custo_final_pf_empreitada']:12.2f}")
    print(f"  Economia Tributária na Empreitada Global p/ PF:  R$ {ex3['economia_empreitada_para_pf']:12.2f}")
    print("=" * 80)


if __name__ == "__main__":
    exibir_relatorio_construcao()
