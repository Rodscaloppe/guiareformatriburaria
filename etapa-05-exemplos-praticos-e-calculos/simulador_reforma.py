"""Simulador Didático da Reforma Tributária (EC 132/2023 e LC 214/2025).

Este módulo implementa os cálculos matemáticos de:
1. Apuração Não Cumulativa do IVA Dual (CBS + IBS) e Split Payment;
2. Regimes Diferenciados (reduções de 30%, 60% e 100%);
3. Regime Específico de Operações Imobiliárias (Venda e Locação com Redutor Social);
4. Verificação de enquadramento de Locador Pessoa Física e Cashback (CadÚnico).
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AliquotaPadrao:
    """Representa as alíquotas de referência da CBS (Federal) e IBS (Estadual/Municipal)."""

    cbs: float = 0.088
    ibs: float = 0.177

    @property
    def total(self) -> float:
        """Retorna a alíquota total do IVA Dual (CBS + IBS)."""
        return round(self.cbs + self.ibs, 6)


@dataclass(frozen=True)
class OperacaoItem:
    """Representa uma compra (entrada) ou venda (saída) de bem ou serviço."""

    descricao: str
    valor_liquido: float
    reducao_aliquota: float = 0.0
    gera_credito: bool = True


@dataclass(frozen=True)
class ResultadoApuracao:
    """Armazena o resumo da apuração mensal de IBS/CBS e Split Payment."""

    total_debitos: float
    total_creditos: float
    imposto_liquido_a_recolher: float
    saldo_credor_a_transportar: float


def calcular_tributo_operacao(
    item: OperacaoItem,
    aliquota: AliquotaPadrao = AliquotaPadrao(),
) -> float:
    """Calcula o valor de IBS + CBS 'por fora' aplicando eventual redução de alíquota."""
    if item.valor_liquido < 0:
        raise ValueError("O valor líquido da operação não pode ser negativo.")
    if not 0.0 <= item.reducao_aliquota <= 1.0:
        raise ValueError("A redução de alíquota deve estar entre 0.0 (0%) e 1.0 (100%).")

    aliquota_efetiva = aliquota.total * (1.0 - item.reducao_aliquota)
    return round(item.valor_liquido * aliquota_efetiva, 2)


def apurar_periodo(
    compras: List[OperacaoItem],
    vendas: List[OperacaoItem],
    aliquota: AliquotaPadrao = AliquotaPadrao(),
) -> ResultadoApuracao:
    """Realiza a apuração não cumulativa (Débitos nas saídas - Créditos nas entradas)."""
    creditos = sum(
        calcular_tributo_operacao(c, aliquota) for c in compras if c.gera_credito
    )
    debitos = sum(calcular_tributo_operacao(v, aliquota) for v in vendas)

    diferenca = round(debitos - creditos, 2)
    imposto_a_recolher = max(0.0, diferenca)
    saldo_credor = max(0.0, round(-diferenca, 2))

    return ResultadoApuracao(
        total_debitos=round(debitos, 2),
        total_creditos=round(creditos, 2),
        imposto_liquido_a_recolher=imposto_a_recolher,
        saldo_credor_a_transportar=saldo_credor,
    )


def calcular_locacao_residencial(
    valor_aluguel: float,
    redutor_social: float = 600.0,
    aliquota: AliquotaPadrao = AliquotaPadrao(),
) -> dict:
    """Calcula o IBS/CBS sobre aluguel residencial (redução de 70% e redutor social de R$ 600)."""
    if valor_aluguel < 0:
        raise ValueError("O valor do aluguel não pode ser negativo.")

    base_calculo = max(0.0, round(valor_aluguel - redutor_social, 2))
    aliquota_locacao = round(aliquota.total * 0.30, 6)
    tributo = round(base_calculo * aliquota_locacao, 2)
    aliquota_efetiva_real = round((tributo / valor_aluguel) * 100, 2) if valor_aluguel > 0 else 0.0

    return {
        "valor_aluguel": valor_aluguel,
        "redutor_social": redutor_social,
        "base_calculo": base_calculo,
        "aliquota_nominal_reduzida_pct": round(aliquota_locacao * 100, 2),
        "tributo_devido": tributo,
        "aliquota_efetiva_pct": aliquota_efetiva_real,
    }


def verificar_contribuinte_locador_pf(
    qtd_imoveis: int,
    receita_anual_alugueis: float,
) -> bool:
    """Verifica se Pessoa Física locadora de imóveis é contribuinte de IBS/CBS (LC 214/2025).

    Regra:
    - No ano anterior: > 3 imóveis distintos E receita > R$ 240.000,00; OU
    - No ano corrente: receita > R$ 288.000,00 (20% acima do limite de R$ 240 mil).
    """
    if qtd_imoveis < 0 or receita_anual_alugueis < 0:
        raise ValueError("Quantidade de imóveis e receita anual não podem ser negativas.")

    regra_ordinaria = qtd_imoveis > 3 and receita_anual_alugueis > 240_000.0
    regra_excesso_ano_corrente = receita_anual_alugueis > 288_000.0
    return regra_ordinaria or regra_excesso_ano_corrente


def exibir_demonstracao() -> None:
    """Executa e imprime três simulações didáticas no terminal."""
    aliquota = AliquotaPadrao(cbs=0.088, ibs=0.177)
    print("=" * 76)
    print("SIMULADOR DIDÁTICO DA REFORMA TRIBUTÁRIA (EC 132/2023 & LC 214/2025)")
    print(f"Alíquota de Referência: CBS={aliquota.cbs*100:.1f}% + IBS={aliquota.ibs*100:.1f}% = {aliquota.total*100:.1f}%")
    print("=" * 76)

    compras = [
        OperacaoItem("Mercadorias para revenda", 100_000.00, reducao_aliquota=0.0),
        OperacaoItem("Energia elétrica e internet", 4_000.00, reducao_aliquota=0.0),
        OperacaoItem("Software ERP e Marketing", 6_000.00, reducao_aliquota=0.0),
        OperacaoItem("Aluguel da loja comercial (-70%)", 10_000.00, reducao_aliquota=0.70),
        OperacaoItem("Festa de lazer pessoal (uso pessoal)", 2_000.00, gera_credito=False),
    ]
    vendas = [
        OperacaoItem("Vendas de mercadorias no mês", 180_000.00, reducao_aliquota=0.0),
    ]

    res = apurar_periodo(compras, vendas, aliquota)
    print("\n[1] APURAÇÃO NÃO CUMULATIVA (COMÉRCIO VAREJISTA):")
    print(f"  (+) Total de Débitos nas Vendas:     R$ {res.total_debitos:10.2f}")
    print(f"  (-) Total de Créditos nas Compras:   R$ {res.total_creditos:10.2f}")
    print(f"  (=) Imposto Líquido via Split/Guia:  R$ {res.imposto_liquido_a_recolher:10.2f}")

    loc = calcular_locacao_residencial(2_600.00, redutor_social=600.0, aliquota=aliquota)
    print("\n[2] LOCAÇÃO RESIDENCIAL (R$ 2.600,00/mês com Redutor Social de R$ 600,00):")
    print(f"  Base de Cálculo após Redutor Social: R$ {loc['base_calculo']:10.2f}")
    print(f"  Alíquota Reduzida (-70%):            {loc['aliquota_nominal_reduzida_pct']:9.2f}%")
    print(f"  IBS + CBS Devido:                    R$ {loc['tributo_devido']:10.2f} ({loc['aliquota_efetiva_pct']}% efetivo)")

    print("\n[3] ENQUADRAMENTO DE PESSOA FÍSICA QUE ALUGA IMÓVEIS:")
    cenarios_pf = [
        ("PF com 2 imóveis e R$ 180 mil/ano", 2, 180_000.0),
        ("PF com 4 imóveis e R$ 200 mil/ano", 4, 200_000.0),
        ("PF com 4 imóveis e R$ 250 mil/ano", 4, 250_000.0),
    ]
    for nome, qtd, rec in cenarios_pf:
        eh_contrib = verificar_contribuinte_locador_pf(qtd, rec)
        status = "CONTRIBUINTE (paga IBS/CBS)" if eh_contrib else "ISENTO / NÃO CONTRIBUINTE"
        print(f"  - {nome:<36} -> {status}")
    print("=" * 76)


if __name__ == "__main__":
    exibir_demonstracao()
