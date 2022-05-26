import csv
from datetime import datetime
from conexion import binanceConnect
import pandas as pd
from chatTelegramClass import ChatTelegram


"""
Se tienen funciones respecto 
a informacion de binance y 
la cuenta propia de binance
"""
cliente = binanceConnect()

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
        print("function::mostrar_precio -> SIMBOLO: " + symbol + " PRECIO: " + price)

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
    if existe == False:
        print('function::existe_par -> No existe ese Par')
    return existe


# muestra todos los datos desde cierta fecha, ordenadamente
def datos_ticker(simbolo, temporalidad,limite=False):
    try:
        existe = existe_par(simbolo)
        if existe == True:
            if limite == False:
                old, new = tiempo_server()
                start_date = str(old)
                klines = cliente.get_historical_klines(symbol=simbolo, interval=temporalidad, start_str=start_date)
            else:
                if temporalidad == cliente.KLINE_INTERVAL_1MINUTE or \
                        temporalidad == cliente.KLINE_INTERVAL_3MINUTE or \
                        temporalidad == cliente.KLINE_INTERVAL_5MINUTE or \
                        temporalidad == cliente.KLINE_INTERVAL_15MINUTE or \
                        temporalidad == cliente.KLINE_INTERVAL_30MINUTE:
                    klines = cliente.get_historical_klines(symbol=simbolo, interval=temporalidad, start_str='%s minutes ago' % limite, limit=limite)
                elif temporalidad == cliente.KLINE_INTERVAL_1HOUR or \
                        temporalidad == cliente.KLINE_INTERVAL_2HOUR or \
                        temporalidad == cliente.KLINE_INTERVAL_4HOUR or \
                        temporalidad == cliente.KLINE_INTERVAL_6HOUR or \
                        temporalidad == cliente.KLINE_INTERVAL_8HOUR or \
                        temporalidad == cliente.KLINE_INTERVAL_12HOUR:
                    klines = cliente.get_historical_klines(symbol=simbolo, interval=temporalidad, start_str='%s hours ago' % limite, limit=limite)
                elif temporalidad == cliente.KLINE_INTERVAL_1DAY or temporalidad == cliente.KLINE_INTERVAL_3DAY:
                    klines = cliente.get_historical_klines(symbol=simbolo, interval=temporalidad, start_str='%s days ago' % limite, limit=limite)
                elif temporalidad == cliente.KLINE_INTERVAL_1WEEK:
                    klines = cliente.get_historical_klines(symbol=simbolo, interval=temporalidad, start_str='%s weeks ago' % limite, limit=limite)
                elif temporalidad == cliente.KLINE_INTERVAL_1MONTH:
                    klines = cliente.get_historical_klines(symbol=simbolo, interval=temporalidad, start_str='%s months ago' % limite, limit=limite)

            data = pd.DataFrame(klines)
            data = data.drop([6, 7, 8, 9, 10], axis=1)
            columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'trades']
            data.columns = columns
            for col in columns:
                data[col] = data[col].astype(float)
            data['timestamp'] = pd.to_datetime(data['timestamp'] * 1000000)
            return data  # retorna un DataFrame
        else:
            return existe
    except Exception as e:
        mensaje = 'ERROR:', e
        print(mensaje)
        ChatTelegram(mensaje)

# Muestra el balance de mi cuenta
def balance():
    try:
        info = cliente.get_account()
        balance = info['balances']
        list_balance = []
        for i in balance:
            if float(i['free']) > 0:
                list_balance.append(i)
                i['precio_compra'] = i['free']
        balance = pd.DataFrame(list_balance)
        return balance
    except Exception as e:
        mensaje = 'ERROR:', e
        print(mensaje)
        ChatTelegram(mensaje)


#genera un CSV
def get_csv(data, simbolo, temporalidad, save=True, star_data=False):
    try:
        if star_data == False:
            filename = '%s-%s-data.csv' % (simbolo, temporalidad)
        else:
            filename = '%s-%s-data-%s.csv' % (simbolo, temporalidad, star_data)
        print('function:get_csv -> Descargando todos los datos %s de %s...' % (temporalidad, simbolo))
        if save:
            data.to_csv(filename)
            print('Datos cargados...')
        return data
    except Exception as e:
        mensaje = 'ERROR:', e
        print(mensaje)
        ChatTelegram(mensaje)
        return None

def leer_csv(simbolo, descripcion):
    try:
        lista_datos = []
        with open('%s-%s-data.csv' % (simbolo, descripcion), newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                lista_datos.append(row)
        datos_df = pd.DataFrame(lista_datos)
        datos_df = datos_df.drop(datos_df.index[[0]])
        return datos_df
    except Exception as e:
        mensaje = 'ERROR:', e
        print(mensaje)
        ChatTelegram(mensaje)
        return None


# saber cantidad minima y maxima de compra
def cantidad_min_max(simbolo):
    existe = existe_par(simbolo)
    if existe == True:
        info = cliente.get_symbol_info(simbolo)
        cant_min = float(info['filters'][2].get('minQty'))
        cant_max = float(info['filters'][2].get('maxQty'))
        min_notional = float(info['filters'][3].get('minNotional'))
        print('function::cantidad_min_max -> Par: ' + simbolo)
        print('Cantidad minima a comprar: ', cant_min)
        print('Cantidad maxima a comprar: ', cant_max)
        print('Cantidad minima a comprar en $: ', min_notional)
        return cant_min, cant_max, min_notional
    else:
        print('No existe ese par')

def  ejecutarOrden(simbolo, BuySell, cantidad,precio):
    try:
       orden =  cliente.create_order(
            symbol=simbolo, #para a comprar
            side=BuySell, #orden de compra o venta
            type='LIMIT', #tipo de orden
            timeInForce='GTC',
            quantity=cantidad, #cantidad en $$
            price=precio #precio para la orden
        )
       idOrden =  orden.get('orderId')
       status = orden.get('status')
       print('function::ejecutaOrden -> Se ejecuto la orden')
       print('function::ejecutaOrden -> ID: ', idOrden,' status: ', status)
       return idOrden, status

    except Exception as e:
        mensaje = 'ERROR -> ejecutarOrden: ',e
        print(mensaje)
        ChatTelegram(mensaje)
        return None, None

def cancelarOrden(simbolo, id):
    orden = cliente.cancel_order(symbol=simbolo, orderId=id)
    idOrden = orden.get('orderId')
    status = orden.get('status')
    print('function::cancelarOrden -> Se cancelo la orden')
    print('function::cancelarOrden -> ID: ', idOrden, ' status: ', status)
    return idOrden, status

def getStatusOrden(simbolo, id):
    orden = cliente.get_order(symbol=simbolo, orderId=id)
    idOrden = orden.get('orderId')
    status = orden.get('status')
    print('function::getStatusOrden -> Se cancelo la orden')
    print('function::getStatusOrden -> ID: ', idOrden, ' status: ', status)
    return idOrden, status

"""
TIPOS DE STATUS:
    NEW
    CANCELED
    FILLED
"""

