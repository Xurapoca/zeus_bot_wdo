
# definindo o tempo de espera
tempo_espera = 20 # em minutos
#armazenando o tempo atual em segundos
tempo_atual = time.time()
#armazenando tempo do ultimo toque no preço anterior
tempo_toque_anterior = 0
#verificando se ja passou o tempo de espera para uma nova operaçao no mesmo nivel de preço
if tempo_atual - tempo_toque_anterior > tempo_espera*60:
    # executar a operaçao
    #...
    #atualizar o tempo do ultimo toque no preço anterior
    tempo_toque_anterior = tempo_atual




import datetime
import numpy as np
import pandas as pd


from iqoptionapi.stable_api import IQ_Option
import sys
import math
import talib
import traceback
import smarttbot_lib.trading_system as ts
# Obter tempo do toque no preço anterior
timestamp = 0
cdl_shooting_star = talib.CDLSHOOTINGSTAR(high, low, open, close)
if cdl_shooting_star[-2] == 100:
    timestamp = timestamp_ant


# definiçao de variaveis:


# Lotes
lotes = 3

# Limite de perda diária
limite_perda = 500

# Limite de ganho diário
limite_ganho = 500
# Stop loss em pontos
sl = 4

# Gain em pontos
gain = 5

# Stop loss em pontos para a vwap band
sl_vwap = [4, 5, 7]

# Gain em pontos para a vwap band
gain_vwap = [5, 10, 30]

# Definição de variáveis para operação
compra = False
venda = False
preco_referencia = 0
preco_referencia_invertido = 0
stop_loss = 0
take_profit = 0
touched = False

# Conexão com IQ Option
API = IQ_Option.IQOption("email", "senha")
API.connect()

# Loop infinito para operação
while True:
    # Checagem do horário
    hora_atual = int(datetime.datetime.now().strftime("%H%M%S"))
    if hora_atual < 60000 or hora_atual > 220000:
        continue

    # Obtenção do preço atual
    preco_atual = API.get_best_candles("WDOJ23", 60)[-1]["close"]

    # Checagem da primeira vez que o preço tocou o preço de referência
    if not touched:
        if preco_atual <= preco_referencia:
            touched = True
            stop_loss = preco_referencia + 0.002
            take_profit = preco_referencia - 0.001
            compra = True
        elif preco_atual >= preco_referencia:
            touched = True
            stop_loss = preco_referencia - 0.002
            take_profit = preco_referencia + 0.001
            venda = True

    # Checagem para inverter a operação caso o preço rompa o preço de referência
    if touched:
        if compra and preco_atual > preco_referencia_invertido:
            compra = False
            venda = True
            preco_referencia = preco_referencia_invertido
            stop_loss = preco_referencia - 0.002
            take_profit = preco_referencia + 0.001
        elif venda and preco_atual < preco_referencia_invertido:
            compra = True
            venda = False
            preco_referencia = preco_referencia_invertido
            stop_loss = preco_referencia + 0.002
            take_profit = preco_referencia - 0.001

    # Execução da operação de compra ou venda
    if compra:
        if API.buy(3, "WDOJ23", "call", 1):
            print("Compra executada")
            preco_referencia_invertido = preco_referencia
            preco_referencia = preco_atual
            touched = False
    elif venda:
        if API.buy(3, "WDOJ23", "put", 1):
            print("Venda executada")
            preco_referencia_invertido = preco_referencia
            preco_referencia = preco_atual
            touched = False

    # Checagem de limite de perda diária
    if API.get_balance() - limite_perda <= API.get_balance_changes():
        break

    # Checagem de limite de ganho diário
    if API.get_balance_changes() >= limite_ganho:
        break

    # Intervalo de tempo para próxima iteração
    time.sleep(0.5)



#Declaração das variáveis de compra
comprado = False
preco_compra = 0
stop_loss_compra = 0
take_profit_compra = 0


# Declaração das variáveis de venda
vendido = False
preco_venda = 0
stop_loss_venda = 0
take_profit_venda = 0



# Definindo os níveis de suporte e resistência
# com base nos preços dos últimos 20 ajustes diários


prices = api.get_adjusted_close_prices('MINIDOLAR', 21)[:-1]

supports = []
resistances = []

for i in range(1, len(prices[0])):
    period = prices[:, i - 1:i + 4]
    max_price = np.max(period)
    min_price = np.min(period)
    pivot = prices[1, i - 1]

    if pivot > max_price:
        resistances.append(max_price)
        supports.append(min_price)
    elif pivot < min_price:
        resistances.append(max_price)
        supports.append(min_price)
    else:
        resistances.append(np.nan)
        supports.append(np.nan)

supports = supports[-20:]
resistances = resistances[-20:]
