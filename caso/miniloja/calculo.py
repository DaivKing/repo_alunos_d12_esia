"""Cálculo de totais de pedido."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula o total do pedido (caso/regras.md, R1).

    Args:
        itens: lista de dicts com "preco" (float) e "qtd" (int); pode ser vazia.
        cupom: "PROMO10" (10%), "VIP15" (15%), "NATAL" (20%, só com a variável de
            ambiente MINILOJA_PROMO_NATAL=1, lida a cada chamada), "FRETEGRATIS"
            (não altera o valor, zera o frete) ou None. Cupom desconhecido é ignorado.
        uf: PE, SP, RJ ou outra; define frete e taxa de serviço (UF desconhecida usa
            o frete e a taxa padrão).

    Ordem: subtotal, desconto, frete, taxa de serviço sobre (subtotal com desconto +
    frete), arredondamento final.

    Returns:
        float com duas casas decimais (round).

    Divergências conhecidas em relação ao contrato, preservadas de propósito (o
    comportamento atual é o golden master; ver ADR 0001): o frete é grátis só com
    subtotal com desconto > 200 (o contrato diz >= 200) e o arredondamento é o do
    round() do Python, não "meio para cima".
    """
    # soma dos itens
    total = 0
    for i in itens:
        preco = i["preco"]
        qtd = i["qtd"]
        total = total + preco * qtd
    # total = round(total, 2)  # tentamos arredondar aqui em 2023, desfeito

    # desconto
    desconto_aplicado = False
    if cupom is not None:
        if cupom == "PROMO10":
            total = total * 0.9
            desconto_aplicado = True
        elif cupom == "VIP15":
            total = total * 0.85
            desconto_aplicado = True
        elif cupom == "FRETEGRATIS":
            # tratado mais abaixo
            desconto_aplicado = False
        elif cupom == "NATAL":
            # campanha antiga; só vale se a flag estiver ligada
            if flags.promo_natal_ativa():
                total = total * 0.8
                desconto_aplicado = True
            else:
                desconto_aplicado = False
        else:
            # cupom desconhecido é ignorado
            desconto_aplicado = False

    # frete
    frete = 0
    if cupom == "FRETEGRATIS":
        frete = 0
    else:
        if total > 200:
            frete = 0
        else:
            if uf == "PE":
                frete = 12.9
            elif uf == "SP":
                frete = 19.9
            elif uf == "RJ":
                frete = 21.5
            else:
                frete = 29.9
    total = total + frete

    # taxa de serviço por UF
    if uf == "PE":
        taxa = 0.05
    elif uf == "SP":
        taxa = 0.07
    elif uf == "RJ":
        taxa = 0.06
    else:
        taxa = 0.08
    imposto = total * taxa
    total = total + imposto

    if desconto_aplicado:
        pass  # reservado para relatório de descontos (não implementado)

    return round(total, 2)
