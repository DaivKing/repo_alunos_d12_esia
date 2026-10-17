"""Cadastro de clientes."""

import re

_CLIENTES = []
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


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
    erros = []
    nome = payload.get("nome")
    if not isinstance(nome, str) or not nome.strip():
        erros.append({"campo": "nome", "erro": "nome obrigatório"})
    email = payload.get("email")
    if not isinstance(email, str) or not email.strip():
        erros.append({"campo": "email", "erro": "email obrigatório"})
    elif not _EMAIL_RE.match(email):
        erros.append({"campo": "email", "erro": "email inválido"})
    cpf = payload.get("cpf")
    if cpf is None or (isinstance(cpf, str) and not cpf.strip()):
        erros.append({"campo": "cpf", "erro": "cpf obrigatório"})
    elif not _cpf_valido(cpf):
        erros.append({"campo": "cpf", "erro": "cpf inválido"})
    if erros:
        return 422, {"erros": erros}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
