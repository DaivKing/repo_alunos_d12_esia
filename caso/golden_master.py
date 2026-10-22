#!/usr/bin/env python3
"""Golden master de calcular_total (AV2, caminho B).

--gerar    grava caso/golden_calculo.json a partir do código ATUAL (rodar uma única vez,
           com o código original, antes de refatorar).
--comparar recalcula cada entrada do JSON e exige igualdade EXATA (==, sem tolerância)
           e tipo float. Sai com 1 se houver qualquer diferença.

Uso, na raiz do repositório: python -B caso/golden_master.py --gerar|--comparar
"""
import itertools
import json
import os
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from miniloja.calculo import calcular_total  # noqa: E402

JSON = AQUI / "golden_calculo.json"

CARRINHOS = {
    "vazio": [],
    "um_item_19_99_x3": [{"preco": 19.99, "qtd": 3}],
    "subtotal_199_99": [{"preco": 199.99, "qtd": 1}],
    "subtotal_200_00": [{"preco": 200.0, "qtd": 1}],
    "subtotal_200_01": [{"preco": 200.01, "qtd": 1}],
    "200_00_em_dois_itens": [{"preco": 100.0, "qtd": 2}],
    "centavos_0_20": [{"preco": 0.2, "qtd": 1}],
    "centavos_33_33_x3": [{"preco": 33.33, "qtd": 3}],
    "varios_itens": [
        {"preco": 29.9, "qtd": 2},
        {"preco": 15.45, "qtd": 3},
        {"preco": 99.99, "qtd": 1},
        {"preco": 0.99, "qtd": 7},
    ],
    "50_x2": [{"preco": 50.0, "qtd": 2}],
    "80_x1": [{"preco": 80.0, "qtd": 1}],
    "60_x1": [{"preco": 60.0, "qtd": 1}],
    "250_x1": [{"preco": 250.0, "qtd": 1}],
    # cruzam o limite de 200 depois do desconto
    "220_x1": [{"preco": 220.0, "qtd": 1}],
    "222_23_x1": [{"preco": 222.23, "qtd": 1}],
    "235_30_x1": [{"preco": 235.3, "qtd": 1}],
    "250_01_x1": [{"preco": 250.01, "qtd": 1}],
    "preco_alto_qtd_alta": [{"preco": 1234.56, "qtd": 10}],
}
CUPONS = [None, "PROMO10", "VIP15", "FRETEGRATIS", "NATAL", "CUPOMFALSO", "", "promo10"]
UFS = ["PE", "SP", "RJ", "XX", "pe", ""]
FLAGS = ["ausente", "0", "1"]  # MINILOJA_PROMO_NATAL


def chamar(itens, cupom, uf, flag):
    """Executa calcular_total com a flag NATAL no estado pedido e restaura o ambiente."""
    antes = os.environ.get("MINILOJA_PROMO_NATAL")
    try:
        if flag == "ausente":
            os.environ.pop("MINILOJA_PROMO_NATAL", None)
        else:
            os.environ["MINILOJA_PROMO_NATAL"] = flag
        return calcular_total(itens, cupom, uf)
    finally:
        if antes is None:
            os.environ.pop("MINILOJA_PROMO_NATAL", None)
        else:
            os.environ["MINILOJA_PROMO_NATAL"] = antes


def gerar():
    registros = []
    for (nome, itens), cupom, uf, flag in itertools.product(CARRINHOS.items(), CUPONS, UFS, FLAGS):
        registros.append({
            "carrinho": nome, "itens": itens, "cupom": cupom, "uf": uf, "flag": flag,
            "resultado": chamar(itens, cupom, uf, flag),
        })
    JSON.write_text(json.dumps(registros, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"golden gerado: {len(registros)} entradas em {JSON.name}")


def comparar():
    registros = json.loads(JSON.read_text(encoding="utf-8"))
    diferencas = []
    for r in registros:
        obtido = chamar(r["itens"], r["cupom"], r["uf"], r["flag"])
        if not (obtido == r["resultado"] and type(obtido) is float and type(r["resultado"]) is float):
            diferencas.append((r, obtido))
    print(f"entradas: {len(registros)} | iguais: {len(registros) - len(diferencas)} | diferentes: {len(diferencas)}")
    for r, obtido in diferencas[:20]:
        print(f"  DIFERE {r['carrinho']} cupom={r['cupom']!r} uf={r['uf']!r} flag={r['flag']}: "
              f"golden={r['resultado']!r} obtido={obtido!r}")
    return 1 if diferencas else 0


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) == 2 else ""
    if modo == "--gerar":
        gerar()
    elif modo == "--comparar":
        sys.exit(comparar())
    else:
        sys.exit(__doc__)
