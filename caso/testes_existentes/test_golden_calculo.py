import json
import os
import unittest

from miniloja.calculo import calcular_total

CAMINHO_GOLDEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "golden_calculo.json")


def carregar_cenarios():
    with open(CAMINHO_GOLDEN, encoding="utf-8") as f:
        return json.load(f)["cenarios"]


class TestGoldenCalculo(unittest.TestCase):
    """Golden master: as saídas foram geradas pelo código atual, não pelo contrato.

    Cenários com "nota" divergem de caso/regras.md; o valor gravado é o do código.
    """

    def test_cenarios_golden(self):
        cenarios = carregar_cenarios()
        self.assertGreater(len(cenarios), 0)
        for cenario in cenarios:
            with self.subTest(cenario["id"]):
                entrada = cenario["entrada"]
                kwargs = {"uf": entrada["uf"]} if "uf" in entrada else {}
                anterior = os.environ.get("MINILOJA_PROMO_NATAL")
                if entrada["natal_ativa"]:
                    os.environ["MINILOJA_PROMO_NATAL"] = "1"
                else:
                    os.environ.pop("MINILOJA_PROMO_NATAL", None)
                try:
                    resultado = calcular_total(entrada["itens"], entrada["cupom"], **kwargs)
                finally:
                    if anterior is None:
                        os.environ.pop("MINILOJA_PROMO_NATAL", None)
                    else:
                        os.environ["MINILOJA_PROMO_NATAL"] = anterior
                self.assertEqual(resultado, cenario["saida"])


if __name__ == "__main__":
    unittest.main()
