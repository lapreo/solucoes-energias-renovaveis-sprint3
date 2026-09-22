"""pytest -q — roda em Python comum, sem precisar do Pico nem do Wokwi."""
import pytest

from logica import calcular_disponivel, decidir_estado, formatar_linha, representar


@pytest.mark.parametrize("geracao,consumo,disponivel_esperado,status_esperado", [
    (4000, 1500, 2500, "RECARGA AUTORIZADA"),   # Situação 1 do enunciado
    (1800, 1500, 300, "RECARGA REDUZIDA"),      # Situação 2 do enunciado
    (1000, 1800, -800, "RECARGA BLOQUEADA"),    # Situação 3 do enunciado
])
def test_tres_situacoes_oficiais_do_enunciado(geracao, consumo, disponivel_esperado, status_esperado):
    disponivel = calcular_disponivel(geracao, consumo)
    assert disponivel == disponivel_esperado
    status, _cor = decidir_estado(disponivel)
    assert status == status_esperado


def test_fronteiras_dos_tres_estados():
    assert decidir_estado(0)[0] == "RECARGA BLOQUEADA"       # exatamente 0 -> bloqueada
    assert decidir_estado(-1)[0] == "RECARGA BLOQUEADA"
    assert decidir_estado(1)[0] == "RECARGA REDUZIDA"        # logo acima de 0 -> reduzida
    assert decidir_estado(1999)[0] == "RECARGA REDUZIDA"
    assert decidir_estado(2000)[0] == "RECARGA AUTORIZADA"   # exatamente o limite -> autorizada
    assert decidir_estado(2001)[0] == "RECARGA AUTORIZADA"


def test_cores_dos_leds():
    assert decidir_estado(3000)[1] == "verde"
    assert decidir_estado(500)[1] == "amarelo"
    assert decidir_estado(-100)[1] == "vermelho"


def test_representacao_bate_com_o_exemplo_do_enunciado():
    binario, hexadecimal = representar(10, bits=16)
    # o enunciado mostra 10 -> binario 1010, hex 0A (sem os zeros à esquerda);
    # aqui usamos 16 bits fixos, então conferimos que os últimos dígitos batem.
    assert binario.endswith("1010")
    assert hexadecimal.endswith("0A")


def test_representacao_de_negativo_usa_complemento_de_dois():
    binario, hexadecimal = representar(-800, bits=16)
    assert len(binario) == 16 and len(hexadecimal) == 4
    # complemento de dois de -800 em 16 bits: 65536 - 800 = 64736 = 0xFCE0
    assert hexadecimal == "FCE0"
    assert binario == "1111110011100000"


def test_formatar_linha_no_formato_do_enunciado():
    linha = formatar_linha(4000, 1500, 2500, "RECARGA AUTORIZADA")
    assert linha == "GERACAO: 4000 W CONSUMO: 1500 W DISPONIVEL: 2500 W  STATUS: RECARGA AUTORIZADA"
