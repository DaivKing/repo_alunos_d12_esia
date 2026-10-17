"""Cadastro de clientes."""

_CLIENTES = []


def _cpf_valido(cpf):
    digitos = [int(c) for c in str(cpf) if c.isdigit()]
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    for tamanho in (9, 10):
        soma = sum(d * p for d, p in zip(digitos[:tamanho], range(tamanho + 1, 1, -1)))
        if (soma * 10) % 11 % 10 != digitos[tamanho]:
            return False
    return True


def cadastrar_cliente(payload):
    """Cadastra um cliente."""
    if not payload.get("nome"):
        return 400, {"erro": "payload inválido"}
    if not payload.get("email"):
        return 400, {"erro": "payload inválido"}
    if "cpf" in payload and not _cpf_valido(payload["cpf"]):
        return 422, {"erros": [{"campo": "cpf", "erro": "cpf inválido"}]}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
