"""Controle Inteligente de Sessao de Recarga — Raspberry Pi Pico (MicroPython).

Versao DEMONSTRACAO: percorre, em loop, os 3 cenarios EXATOS do enunciado (mesmos
numeros dos exemplos), acendendo o LED certo e imprimindo os dados a cada troca.
Use esta versao para gravar o video — garante que as tres situacoes obrigatorias
apareçam, sem depender de girar potenciometro na hora certa.

Ligacoes (as mesmas de main.py, mas sem os potenciometros):
  LED verde    -> GP16 (com resistor)
  LED amarelo  -> GP17 (com resistor)
  LED vermelho -> GP18 (com resistor)
"""
from machine import Pin
from time import sleep

from logica import calcular_disponivel, decidir_estado, formatar_linha, representar

LED_VERDE = Pin(16, Pin.OUT)
LED_AMARELO = Pin(17, Pin.OUT)
LED_VERMELHO = Pin(18, Pin.OUT)

# Os tres cenarios do enunciado, na ordem: (geracao_w, consumo_w, rotulo)
CENARIOS = [
    (4000, 1500, "Situacao 1 - Energia suficiente"),
    (1800, 1500, "Situacao 2 - Energia limitada"),
    (1000, 1800, "Situacao 3 - Energia insuficiente"),
]

SEGUNDOS_POR_CENARIO = 4


def apagar_leds() -> None:
    LED_VERDE.value(0)
    LED_AMARELO.value(0)
    LED_VERMELHO.value(0)


def acender_led(cor: str) -> None:
    apagar_leds()
    {"verde": LED_VERDE, "amarelo": LED_AMARELO, "vermelho": LED_VERMELHO}[cor].value(1)


def rodar_cenario(rotulo: str, geracao_w: float, consumo_w: float) -> None:
    disponivel_w = calcular_disponivel(geracao_w, consumo_w)
    status, cor = decidir_estado(disponivel_w)
    acender_led(cor)

    print(f"\n--- {rotulo} ---")
    print(formatar_linha(geracao_w, consumo_w, disponivel_w, status))
    binario, hexadecimal = representar(int(disponivel_w))
    print(f"  Representacao de DISPONIVEL ({int(disponivel_w)} W) -> Decimal: {int(disponivel_w)}  Binario: {binario}  Hexadecimal: 0x{hexadecimal}")


def main() -> None:
    print("=== ChargeGrid Intelligence - Demonstracao das 3 situacoes (enunciado) ===")
    while True:
        for rotulo, geracao_w, consumo_w in CENARIOS:
            rodar_cenario(rotulo, geracao_w, consumo_w)
            sleep(SEGUNDOS_POR_CENARIO)


if __name__ == "__main__":
    main()
