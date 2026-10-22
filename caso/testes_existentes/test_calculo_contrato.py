"""Testes de calcular_total derivados de caso/regras.md (R1), não do código.

O valor esperado de cada teste está calculado à mão no comentário, com arredondamento
a duas casas, meio para cima. Escolhi entradas que não caem num meio exato (x,xx5), para o
resultado não depender do erro binário do float; os dois casos em que isso importa estão
nos testes expectedFailure no fim do arquivo.
"""
import os
import unittest

from miniloja.calculo import calcular_total

CEM = [{"preco": 50.0, "qtd": 2}]  # subtotal 100,00


class TestContratoR1(unittest.TestCase):
    def setUp(self):
        antes = os.environ.pop("MINILOJA_PROMO_NATAL", None)
        self.addCleanup(self._restaurar_flag, antes)

    @staticmethod
    def _restaurar_flag(valor):
        if valor is None:
            os.environ.pop("MINILOJA_PROMO_NATAL", None)
        else:
            os.environ["MINILOJA_PROMO_NATAL"] = valor

    # R1.1 subtotal
    def test_r1_1_subtotal_soma_preco_vezes_quantidade(self):
        itens = [{"preco": 10.0, "qtd": 3}, {"preco": 20.0, "qtd": 2}]
        # subtotal 10*3 + 20*2 = 70; SP: (70 + 19,90) * 1,07 = 96,193 -> 96,19
        self.assertEqual(calcular_total(itens, None, "SP"), 96.19)

    def test_r1_1_carrinho_vazio_paga_so_frete_e_taxa(self):
        # subtotal 0; RJ: (0 + 21,50) * 1,06 = 22,79
        self.assertEqual(calcular_total([], None, "RJ"), 22.79)

    # R1.2 cupons
    def test_r1_2_promo10_desconta_10_por_cento(self):
        # 100 * 0,90 = 90; SP: (90 + 19,90) * 1,07 = 117,593 -> 117,59
        self.assertEqual(calcular_total(CEM, "PROMO10", "SP"), 117.59)

    def test_r1_2_vip15_desconta_15_por_cento(self):
        # 100 * 0,85 = 85; SP: (85 + 19,90) * 1,07 = 112,243 -> 112,24
        self.assertEqual(calcular_total(CEM, "VIP15", "SP"), 112.24)

    def test_r1_2_natal_com_campanha_ativa_desconta_20_por_cento(self):
        os.environ["MINILOJA_PROMO_NATAL"] = "1"
        # 100 * 0,80 = 80; RJ: (80 + 21,50) * 1,06 = 107,59
        self.assertEqual(calcular_total(CEM, "NATAL", "RJ"), 107.59)

    def test_r1_2_natal_sem_campanha_nao_desconta(self):
        # sem variável: 100; RJ: (100 + 21,50) * 1,06 = 128,79
        self.assertEqual(calcular_total(CEM, "NATAL", "RJ"), 128.79)
        os.environ["MINILOJA_PROMO_NATAL"] = "0"
        self.assertEqual(calcular_total(CEM, "NATAL", "RJ"), 128.79)

    def test_r1_2_natal_le_a_campanha_a_cada_chamada(self):
        os.environ["MINILOJA_PROMO_NATAL"] = "1"
        ligada = calcular_total(CEM, "NATAL", "RJ")  # 107,59
        os.environ["MINILOJA_PROMO_NATAL"] = "0"
        desligada = calcular_total(CEM, "NATAL", "RJ")  # 128,79
        os.environ["MINILOJA_PROMO_NATAL"] = "1"
        religada = calcular_total(CEM, "NATAL", "RJ")  # 107,59
        self.assertEqual((ligada, desligada, religada), (107.59, 128.79, 107.59))

    def test_r1_2_fretegratis_zera_o_frete_sem_alterar_o_valor(self):
        # subtotal 100 (< 200), sem frete; SP: 100 * 1,07 = 107,00; XX: 100 * 1,08 = 108,00
        self.assertEqual(calcular_total(CEM, "FRETEGRATIS", "SP"), 107.0)
        self.assertEqual(calcular_total(CEM, "FRETEGRATIS", "XX"), 108.0)

    def test_r1_2_cupom_desconhecido_e_ignorado(self):
        # igual a sem cupom; RJ: (100 + 21,50) * 1,06 = 128,79
        self.assertEqual(calcular_total(CEM, "CUPOMFALSO", "RJ"), 128.79)
        self.assertEqual(calcular_total(CEM, None, "RJ"), 128.79)

    # R1.3 e R1.4 frete e taxa por UF (sem cupom, subtotal < 200)
    def test_r1_3_4_pe_frete_12_90_taxa_5_por_cento(self):
        itens = [{"preco": 87.10, "qtd": 1}]
        # (87,10 + 12,90) * 1,05 = 105,00
        self.assertEqual(calcular_total(itens, None, "PE"), 105.0)

    def test_r1_3_4_sp_frete_19_90_taxa_7_por_cento(self):
        # (100 + 19,90) * 1,07 = 128,293 -> 128,29
        self.assertEqual(calcular_total(CEM, None, "SP"), 128.29)

    def test_r1_3_4_rj_frete_21_50_taxa_6_por_cento(self):
        # (100 + 21,50) * 1,06 = 128,79
        self.assertEqual(calcular_total(CEM, None, "RJ"), 128.79)

    def test_r1_3_4_demais_ufs_frete_29_90_taxa_8_por_cento(self):
        # (100 + 29,90) * 1,08 = 140,292 -> 140,29
        self.assertEqual(calcular_total(CEM, None, "XX"), 140.29)

    # R1.3 frete grátis pelo valor, R1.6 ordem
    def test_r1_3_acima_do_limite_nao_paga_frete(self):
        # 250 >= 200, sem frete; SP: 250 * 1,07 = 267,50
        self.assertEqual(calcular_total([{"preco": 250.0, "qtd": 1}], None, "SP"), 267.5)

    def test_r1_6_desconto_que_derruba_o_subtotal_abaixo_de_200_passa_a_pagar_frete(self):
        itens = [{"preco": 220.0, "qtd": 1}]
        # sem cupom: 220 >= 200, sem frete; SP: 220 * 1,07 = 235,40
        self.assertEqual(calcular_total(itens, None, "SP"), 235.4)
        # PROMO10: 220 * 0,90 = 198 (< 200), paga frete: (198 + 19,90) * 1,07 = 233,153 -> 233,15
        self.assertEqual(calcular_total(itens, "PROMO10", "SP"), 233.15)

    def test_r1_6_desconto_que_mantem_acima_de_200_continua_sem_frete(self):
        # 250 * 0,90 = 225 (>= 200), sem frete; PE: 225 * 1,05 = 236,25
        self.assertEqual(calcular_total([{"preco": 250.0, "qtd": 1}], "PROMO10", "PE"), 236.25)

    # Divergências entre o contrato e o código atual: o esperado é o do CONTRATO.
    @unittest.expectedFailure
    def test_r1_3_subtotal_exatamente_200_tem_frete_gratis(self):
        # Divergência R1.3 — reportada, não corrigida; ver ADR 0001.
        # O código usa "total > 200"; o contrato diz "maior ou igual a R$ 200,00".
        # 200 >= 200, sem frete; PE: 200 * 1,05 = 210,00 (o código devolve 223,55)
        self.assertEqual(calcular_total([{"preco": 200.0, "qtd": 1}], None, "PE"), 210.0)

    @unittest.expectedFailure
    def test_r1_5_arredondamento_meio_para_cima(self):
        # Divergência R1.5 — reportada, não corrigida; ver ADR 0001.
        # O código usa round() sobre float; o contrato pede meio para cima.
        # (0,20 + 12,90) * 1,05 = 13,755 -> 13,76
        self.assertEqual(calcular_total([{"preco": 0.20, "qtd": 1}], None, "PE"), 13.76)


if __name__ == "__main__":
    unittest.main()
