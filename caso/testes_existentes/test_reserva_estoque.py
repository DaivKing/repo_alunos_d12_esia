"""Regressão de R2.2: se algum item não tem estoque, o pedido é recusado e
nenhuma reserva feita naquela chamada pode permanecer.

Usa Estoque, GatewayFake e RepositorioPedidos reais (sem MagicMock no estoque).
Os esperados vêm de caso/regras.md (R2.2), não do código.
"""
import unittest

from miniloja.estoque import Estoque, EstoqueInsuficiente
from miniloja.pagamentos import GatewayFake
from miniloja.pedidos import PedidoService
from miniloja.repositorio import RepositorioPedidos


class TestReservaEstoque(unittest.TestCase):
    def setUp(self):
        self.estoque = Estoque({"BOLA-01": 10, "CHUTEIRA-42": 5})
        self.gateway = GatewayFake()
        self.repo = RepositorioPedidos()
        self.svc = PedidoService(self.repo, self.estoque, self.gateway)

    def _item(self, sku, qtd, preco=10.0):
        return {"sku": sku, "preco": preco, "qtd": qtd}

    def test_item_sem_estoque_nao_deixa_reserva(self):
        # (a) R2.2: recusa, nenhuma reserva permanece; nada cobrado nem salvo.
        itens = [self._item("BOLA-01", 2), self._item("CHUTEIRA-42", 999, 100.0)]
        with self.assertRaises(EstoqueInsuficiente) as ctx:
            self.svc.criar(1, itens)
        self.assertEqual(str(ctx.exception), "CHUTEIRA-42")
        self.assertEqual(self.estoque.saldo("BOLA-01"), 10)
        self.assertEqual(self.estoque.saldo("CHUTEIRA-42"), 5)
        self.assertEqual(self.estoque.reservas, {})
        self.assertEqual(self.gateway.cobrancas, [])
        self.assertEqual(self.repo.todos(), [])

    def test_sku_repetido_restaura_saldo_exato(self):
        # (b) mesmo SKU antes do item sem estoque: a chave de reservas é
        # sobrescrita, mas o saldo precisa voltar exatamente ao inicial.
        itens = [
            self._item("BOLA-01", 2),
            self._item("BOLA-01", 3),
            self._item("CHUTEIRA-42", 999, 100.0),
        ]
        with self.assertRaises(EstoqueInsuficiente) as ctx:
            self.svc.criar(1, itens)
        self.assertEqual(str(ctx.exception), "CHUTEIRA-42")
        self.assertEqual(self.estoque.saldo("BOLA-01"), 10)
        self.assertEqual(self.estoque.reservas, {})

    def test_sku_repetido_falha_no_proprio_sku(self):
        # (b2) 6 + 6 > 10: cada item isolado cabe, a soma não.
        itens = [self._item("BOLA-01", 6), self._item("BOLA-01", 6)]
        with self.assertRaises(EstoqueInsuficiente) as ctx:
            self.svc.criar(1, itens)
        self.assertEqual(str(ctx.exception), "BOLA-01")
        self.assertEqual(self.estoque.saldo("BOLA-01"), 10)
        self.assertEqual(self.estoque.reservas, {})

    def test_pedido_com_estoque_continua_reservando(self):
        # (c) guarda de regressão: PASSA antes e depois da correção.
        itens = [self._item("BOLA-01", 2), self._item("CHUTEIRA-42", 1)]
        pedido = self.svc.criar(1, itens)
        # Vêm do contrato e do significado de "reservar": saldo, cobrança, repositório.
        self.assertEqual(pedido["status"], "pago")
        self.assertEqual(self.estoque.saldo("BOLA-01"), 8)
        self.assertEqual(self.estoque.saldo("CHUTEIRA-42"), 4)
        self.assertEqual(len(self.gateway.cobrancas), 1)
        self.assertEqual(len(self.repo.todos()), 1)
        # Caracterização do comportamento ATUAL (chaves "tmp-1"), não do contrato.
        self.assertEqual(
            self.estoque.reservas,
            {("tmp-1", "BOLA-01"): 2, ("tmp-1", "CHUTEIRA-42"): 1},
        )


if __name__ == "__main__":
    unittest.main()
