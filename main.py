"""Controle Inteligente de Sessao de Recarga — Raspberry Pi Pico (MicroPython).

Versao INTERATIVA: dois potenciometros simulam a potencia de geracao e de consumo.
Gire os potenciometros no Wokwi e o sistema recalcula a cada segundo.

Ligacoes (ver diagram.json):
  LED verde    -> GP16 (com resistor)
  LED amarelo  -> GP17 (com resistor)
  LED vermelho -> GP18 (com resistor)
  Potenciometro GERACAO -> GP26 (ADC0)
  Potenciometro CONSUMO -> GP27 (ADC1)

Para a versao com cenarios fixos (mais facil de gravar o video mostrando os 3
exemplos exatos do enunciado), use demo_cenarios.py no lugar deste arquivo.
"""
from machine import ADC, Pin
from time import sleep

from logica import calcular_disponivel, decidir_estado, formatar_linha, representar

# --- Hardware ---------------------------------------------------------------
LED_VERDE = Pin(16, Pin.OUT)
LED_AMARELO = Pin(17, Pin.OUT)
LED_VERMELHO = Pin(18, Pin.OUT)

POT_GERACAO = ADC(Pin(26))
POT_CONSUMO = ADC(Pin(27))

# Fim de curso do potenciometro (65535 no ADC) equivale a esta potencia simulada.
POTENCIA_MAXIMA_SIMULADA_W = 5000


def ler_potencia_w(adc: ADC) -> int:
    """Le o ADC (0 a 65535, resolucao de 16 bits em MicroPython) e converte para
    Watts, numa escala linear de 0 a POTENCIA_MAXIMA_SIMULADA_W."""
    leitura_bruta = adc.read_u16()  # 0..65535
    return round(leitura_bruta / 65535 * POTENCIA_MAXIMA_SIMULADA_W)


def apagar_leds() -> None:
    LED_VERDE.value(0)
    LED_AMARELO.value(0)
    LED_VERMELHO.value(0)


def acender_led(cor: str) -> None:
    apagar_leds()
    {"verde": LED_VERDE, "amarelo": LED_AMARELO, "vermelho": LED_VERMELHO}[cor].value(1)


def rodar_ciclo(geracao_w: float, consumo_w: float) -> None:
    disponivel_w = calcular_disponivel(geracao_w, consumo_w)
    status, cor = decidir_estado(disponivel_w)
    acender_led(cor)

    print(formatar_linha(geracao_w, consumo_w, disponivel_w, status))
    binario, hexadecimal = representar(int(disponivel_w))
    print(f"  Representacao de DISPONIVEL ({int(disponivel_w)} W) -> Decimal: {int(disponivel_w)}  Binario: {binario}  Hexadecimal: 0x{hexadecimal}")


def main() -> None:
    print("=== ChargeGrid Intelligence - Controle Inteligente de Sessao de Recarga ===")
    print("Gire os potenciometros de geracao e consumo. Recalculando a cada 1s...\n")
    while True:
        geracao_w = ler_potencia_w(POT_GERACAO)
        consumo_w = ler_potencia_w(POT_CONSUMO)
        rodar_ciclo(geracao_w, consumo_w)
        sleep(1)


if __name__ == "__main__":
    main()
