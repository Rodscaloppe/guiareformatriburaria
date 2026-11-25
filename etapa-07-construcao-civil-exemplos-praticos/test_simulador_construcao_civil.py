"""Testes Automatizados para os 3 Exemplos Práticos da Construção Civil (LC 214/2025)."""

import unittest
from simulador_construcao_civil import (
    simular_exemplo_1_incorporacao,
    simular_exemplo_2_empreitada_global_b2b,
    simular_exemplo_3_administracao_vs_empreitada_pf,
)


class TestConstrucaoCivilReforma(unittest.TestCase):
    """Valida a precisão matemática dos 3 exemplos da Construção Civil."""

    def test_exemplo_1_incorporacao_residencial(self) -> None:
        """Valida Redutor de Ajuste, Redutor Social e Créditos na Incorporação."""
        res = simular_exemplo_1_incorporacao()
        self.assertEqual(res["vgv_total"], 5_000_000.00)
        self.assertEqual(res["base_calculo"], 3_000_000.00)
        self.assertEqual(res["debito_bruto"], 397_500.00)
        self.assertEqual(res["total_creditos"], 514_100.00)
        self.assertEqual(res["imposto_liquido_a_pagar"], 0.00)
        self.assertEqual(res["saldo_credor"], 116_600.00)
        self.assertEqual(res["carga_efetiva_cadeia_pct"], 7.95)

    def test_exemplo_2_construtora_empreitada_global_b2b(self) -> None:
        """Valida Empreitada Global B2B e recuperação integral do crédito pelo cliente PJ."""
        res = simular_exemplo_2_empreitada_global_b2b()
        self.assertEqual(res["debito_nf_construtora"], 265_000.00)
        self.assertEqual(res["total_creditos_construtora"], 318_000.00)
        self.assertEqual(res["saldo_credor_construtora"], 53_000.00)
        self.assertEqual(res["credito_industria_cliente"], 265_000.00)
        self.assertEqual(res["custo_liquido_real_industria"], 2_000_000.00)

    def test_exemplo_3_administradora_obras_vs_empreitada_pf(self) -> None:
        """Valida tributação sobre Taxa de Administração e comparativo para cliente PF."""
        res = simular_exemplo_3_administracao_vs_empreitada_pf()
        self.assertEqual(res["imposto_administradora_sobre_taxa"], 15_900.00)
        self.assertEqual(res["imposto_total_modalidade_administracao"], 219_950.00)
        self.assertEqual(res["custo_final_pf_administracao"], 1_339_950.00)
        self.assertEqual(res["imposto_total_modalidade_empreitada"], 148_400.00)
        self.assertEqual(res["custo_final_pf_empreitada"], 1_268_400.00)
        self.assertEqual(res["economia_empreitada_para_pf"], 71_550.00)


if __name__ == "__main__":
    unittest.main(verbosity=2)
