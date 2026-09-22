"""
    2500 W disponível -> autorizada  (2500 >= 2000)
    300  W disponível -> reduzida    (0 < 300 < 2000)
    -800 W disponível -> bloqueada   (-800 <= 0)

"""
POTENCIA_NOMINAL_RECARGA_W = 2000

VERDE, AMARELO, VERMELHO = "verde", "amarelo", "vermelho"


def calcular_disponivel(geracao_w: float, consumo_w: float) -> float:
    """Energia disponível = Geração − Consumo (pede o enunciado, item 1)."""
    return geracao_w - consumo_w


def decidir_estado(disponivel_w: float) -> tuple[str, str]:
    """Devolve (texto_do_status, cor_do_led) a partir da energia disponível.

    <= 0                              -> bloqueada  (vermelho)
    > 0 e < POTENCIA_NOMINAL_RECARGA_W -> reduzida   (amarelo)
    >= POTENCIA_NOMINAL_RECARGA_W      -> autorizada (verde)
    """
    if disponivel_w <= 0:
        return "RECARGA BLOQUEADA", VERMELHO
    if disponivel_w < POTENCIA_NOMINAL_RECARGA_W:
        return "RECARGA REDUZIDA", AMARELO
    return "RECARGA AUTORIZADA", VERDE


def representar(valor: int, bits: int = 16) -> tuple[str, str]:
    """Decimal (o próprio `valor`), binário e hexadecimal — item 5 do enunciado.

    Números negativos (energia disponível pode ser negativa) são mostrados em
    COMPLEMENTO DE DOIS de `bits` bits, a forma padrão de representar inteiros com
    sinal em hardware — assunto direto de Arquitetura de Computadores.
    """
    limite = 1 << bits
    valor_sem_sinal = valor % limite  # equivalente ao complemento de dois para negativos
    # MicroPython não tem a função format() do CPython; a mesma formatação
    # (zeros à esquerda, largura fixa) funciona embutida na f-string.
    binario = f"{valor_sem_sinal:0{bits}b}"
    hexadecimal = f"{valor_sem_sinal:0{bits // 4}X}"
    return binario, hexadecimal


def formatar_linha(geracao_w: float, consumo_w: float, disponivel_w: float, status: str) -> str:
    """Uma linha no formato exato pedido no enunciado (item 4)."""
    return f"GERACAO: {geracao_w:.0f} W CONSUMO: {consumo_w:.0f} W DISPONIVEL: {disponivel_w:.0f} W  STATUS: {status}"
