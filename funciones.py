from datetime import datetime
from conexion import cliente
import os
import pandas as pd

"""
Se tienen funciones respecto 
a informacion de binance y 
la cuenta propia de binance
"""


# Devuelve la primera fecha (1 Jan 2017) y la fecha actual del servidor
def tiempo_server():
    # primera fecha del server
    old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    # tiempo actual
    time_res = cliente.get_server_time()
    ts = time_res.get('serverTime')
    new = datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print(new)
    # retorna la primera feccha y la fecha actual (str)
    return old, new


# Muestra todos los precios
def mostrar_precios():
    print('LISTA DE TODOS LOS PRECIOS')
    lista_tickers = cliente.get_all_tickers()
    for ticker in lista_tickers:
        symbol = ticker['symbol']
        price = ticker['price']
        print("SIMBOLO: " + symbol + " PRECIO: " + price)


# muestra todos los datos desde cierta feche, ordenadamente
def datos_ticker(simbolo, temporalidad, start_date=False, limite = False):
    try:
        if start_date == False:
            old, new = tiempo_server()
            start_date = str(old)
        if limite == False:
            klines = cliente.get_historical_klines(symbol=simbolo, interval=temporalidad, start_str=start_date)
        else:
            klines = cliente.get_historical_klines(symbol=simbolo, interval=temporalidad, start_str=start_date, limit=limite)
        data = pd.DataFrame(klines)
        data = data.drop([6, 7, 8, 9, 10], axis=1)
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'trades']
        data.columns = columns
        for col in columns:
            data[col] = data[col].astype(float)
        data['timestamp'] = pd.to_datetime(data['timestamp'] * 1000000)

        return data  # retorna un DataFrame
    except Exception as e:
        print('ERROR:', e)


# permite sabes si existe o no el par
def existe_par(simbolo):
    lista_tickers = cliente.get_all_tickers()
    for ticker in lista_tickers:
        symbol = ticker['symbol']
        if symbol == simbolo:
            existe = True
            # TRUE si existe el par
            break
        else:
            existe = False
            # FALSE si no existe el par
    return existe


# Muestra el balance de mi cuenta
def balance():
    try:
        info = cliente.get_account()
        balance = info['balances']
        print('BALANCE DE MI CUENTA ')
        for i in balance:
            if float(i['free']) > 0:
                print(i['asset'] + ' ' + i['free'])
    except Exception as e:
        print('ERROR: ', e)


# guarda los datos de un simbolo en un CSV de un mismo simbolo
def get_data_csv(simbolo, temporalidad, save=True, star_data=False):
    if star_data == False:
        filename = '%s-%s-data_all.csv' % (simbolo, temporalidad)
        old, new = tiempo_server()
        star_data = old
    else:
        filename = '%s-%s-data-%s.csv' % (simbolo, temporalidad, star_data)
    # si existe el archivo lo lee, sino lo crea
    if os.path.isfile(filename):
        data_df = pd.read_csv(filename)
    else:
        data_df = pd.DataFrame()
    print('Descargando todos los datos %s de %s...' % (temporalidad, simbolo))
    # obtiene todos los datos de ese simbolo
    klines = cliente.get_historical_klines(simbolo, temporalidad, str(star_data))
    data = pd.DataFrame(klines)
    data = data.drop([6, 7, 8, 9, 10], axis=1)
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'trades']
    data.columns = columns
    data['timestamp'] = pd.to_datetime(data['timestamp'] * 1000000)
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else:
        data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save:
        data_df.to_csv(filename)
    print('Datos cargados...')
    return data_df


# saber cantidad minima y maxima de compra
def cantidad_min_max(simbolo):
    existe = existe_par(simbolo)
    if existe == True:
        info = cliente.get_symbol_info(simbolo)
        cant_min = float(info['filters'][2].get('minQty'))
        cant_max = float(info['filters'][2].get('maxQty'))
        print('Par: ' + simbolo)
        print('Cantidad minima a comprar: ', cant_min)
        print('Cantidad maxima a comprar: ', cant_max)
        return cant_min, cant_max
    else:
        print('No existe ese par')
