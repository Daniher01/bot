import pandas as pd
import numpy as np
import talib as ta
import indicadores

"""
Clase para realizar los backtesting manualmente
"""

def bt_wma(df, periodo):
    contador = 0
    lista_close = [] #lista para guardar precios de cierra
    lista_wma = [] #lista para guardar las wma de los precios
    for i in df.close:
        contador += 1
        lista_close.append(i)
        npy = np.array(lista_close)
        d = ta.stream_WMA(npy, periodo)
        lista_wma.append(d)
        data_df = pd.DataFrame(lista_wma)
    return data_df

def bt_hma(df, periodo):
    contador = 0
    lista_close = []  # lista para guardar precios de cierra
    lista_wma = []  # lista para guardar las wma de los precios}    for i in df.close:
    for i in df.close:
        contador += 1
        lista_close.append(i)
        data = pd.DataFrame(lista_close)
        data['close'] = data[0]
        d = indicadores.HMA(data, periodo)
        lista_wma.append(d)
        data_df = pd.DataFrame(lista_wma)
    return data_df