import json
import os
import unittest
from pathlib import Path

from miniloja.calculo import calcular_total

GOLDEN = Path(__file__).resolve().parent.parent / "golden_calculo.json"


class TestGoldenCalculo(unittest.TestCase):
    """Golden master: resultados do calcular_total original, igualdade exata (sem tolerância)."""

    def test_todas_as_entradas_do_golden_sao_identicas(self):
        registros = json.loads(GOLDEN.read_text(encoding="utf-8"))
        self.assertGreater(len(registros), 2000)
        antes = os.environ.get("MINILOJA_PROMO_NATAL")
        diferencas = []
        try:
            for r in registros:
                if r["flag"] == "ausente":
                    os.environ.pop("MINILOJA_PROMO_NATAL", None)
                else:
                    os.environ["MINILOJA_PROMO_NATAL"] = r["flag"]
                obtido = calcular_total(r["itens"], r["cupom"], r["uf"])
                if not (obtido == r["resultado"] and type(obtido) is float):
                    diferencas.append((r["carrinho"], r["cupom"], r["uf"], r["flag"], r["resultado"], obtido))
        finally:
            if antes is None:
                os.environ.pop("MINILOJA_PROMO_NATAL", None)
            else:
                os.environ["MINILOJA_PROMO_NATAL"] = antes
        self.assertEqual(diferencas, [], f"{len(diferencas)} diferenças; primeiras: {diferencas[:5]}")
