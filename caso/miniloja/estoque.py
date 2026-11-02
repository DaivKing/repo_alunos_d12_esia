"""Controle de estoque em memória."""


class EstoqueInsuficiente(Exception):
    pass


class Estoque:
    def __init__(self, saldos=None):
        self.saldos = dict(saldos or {})
        self.reservas = {}

    def reservar(self, sku, qtd, pedido_id):
        """Reserva a quantidade do SKU no estoque."""
        disponivel = self.saldos.get(sku, 0)
        if disponivel < qtd:
            raise EstoqueInsuficiente(sku)
        self.saldos[sku] = disponivel - qtd
        self.reservas[(pedido_id, sku)] = qtd
        return True

    def liberar(self, sku, qtd, pedido_id):
        """Desfaz uma reserva: devolve qtd ao saldo e abate a entrada em reservas."""
        self.saldos[sku] = self.saldos.get(sku, 0) + qtd
        chave = (pedido_id, sku)
        restante = self.reservas.get(chave, 0) - qtd
        if restante > 0:
            self.reservas[chave] = restante
        else:
            self.reservas.pop(chave, None)

    def saldo(self, sku):
        return self.saldos.get(sku, 0)
