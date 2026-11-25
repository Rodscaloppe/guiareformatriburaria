"""Testes Automatizados dos Casos de Teste Fiscais (CT-RT-01 a CT-RT-05).

Baseados nas técnicas de Partição de Equivalência, Análise de Valor-Limite (AVL)
e Tabela de Decisão (ISTQB CTFL v4.0 / ISO/IEC/IEEE 29119-3).
"""

import unittest
from simulador_reforma import (
    AliquotaPadrao,
    OperacaoItem,
    apurar_periodo,
    calcular_locacao_residencial,
    calcular_tributo_operacao,
    verificar_contribuinte_locador_pf,
)


class TestSimuladorReformaTributaria(unittest.TestCase):
    """Suíte de validação matemática do motor didático da Reforma Tributária."""

    def setUp(self) -> None:
        self.aliquota = AliquotaPadrao(cbs=0.088, ibs=0.177)

    def test_ct_rt_01_reducao_60_porcento_saude_educacao(self) -> None:
        """CT-RT-01: Redução de 60% na alíquota padrão (26,5% -> 10,6%)."""
        item = OperacaoItem("Serviço Hospitalar", valor_liquido=1000.00, reducao_aliquota=0.60)
        tributo = calcular_tributo_operacao(item, self.aliquota)
        self.assertEqual(tributo, 106.00)

    def test_ct_rt_02_aliquota_zero_cesta_basica(self) -> None:
        """CT-RT-02: Redução de 100% (Alíquota Zero - Cesta Básica Nacional)."""
        item = OperacaoItem("Arroz e Feijão - Cesta Básica", valor_liquido=500.00, reducao_aliquota=1.00)
        tributo = calcular_tributo_operacao(item, self.aliquota)
        self.assertEqual(tributo, 0.00)

    def test_ct_rt_03_valor_limite_redutor_social_locacao(self) -> None:
        """CT-RT-03: Análise de Valor-Limite no Redutor Social de R$ 600,00."""
        res_599 = calcular_locacao_residencial(599.99, redutor_social=600.00, aliquota=self.aliquota)
        res_600 = calcular_locacao_residencial(600.00, redutor_social=600.00, aliquota=self.aliquota)
        res_601 = calcular_locacao_residencial(600.01, redutor_social=600.00, aliquota=self.aliquota)

        self.assertEqual(res_599["base_calculo"], 0.00)
        self.assertEqual(res_599["tributo_devido"], 0.00)
        self.assertEqual(res_600["base_calculo"], 0.00)
        self.assertEqual(res_600["tributo_devido"], 0.00)
        self.assertEqual(res_601["base_calculo"], 0.01)

    def test_ct_rt_04_fronteira_enquadramento_locador_pf(self) -> None:
        """CT-RT-04: Tabela de Decisão e Valor-Limite para Locador Pessoa Física."""
        self.assertFalse(verificar_contribuinte_locador_pf(3, 250_000.00))
        self.assertFalse(verificar_contribuinte_locador_pf(4, 239_999.99))
        self.assertFalse(verificar_contribuinte_locador_pf(4, 240_000.00))
        self.assertTrue(verificar_contribuinte_locador_pf(4, 240_000.01))
        self.assertTrue(verificar_contribuinte_locador_pf(2, 288_000.01))

    def test_ct_rt_05_bloqueio_credito_uso_consumo_pessoal(self) -> None:
        """CT-RT-05: Bens de uso e consumo pessoal não geram crédito de IBS/CBS."""
        compras = [
            OperacaoItem("Insumo produtivo", valor_liquido=1000.00, gera_credito=True),
            OperacaoItem("Item de uso pessoal", valor_liquido=2000.00, gera_credito=False),
        ]
        vendas = [OperacaoItem("Venda produto", valor_liquido=2000.00)]
        apuracao = apurar_periodo(compras, vendas, self.aliquota)

        self.assertEqual(apuracao.total_creditos, 265.00)
        self.assertEqual(apuracao.total_debitos, 530.00)
        self.assertEqual(apuracao.imposto_liquido_a_recolher, 265.00)


if __name__ == "__main__":
    unittest.main(verbosity=2)
