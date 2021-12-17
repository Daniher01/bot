import math
import talib as ta
"""
Se tienen funciones de los indicadores 
que no estan en la libreria TA-Lib

"""

def HMA(df, periodo):
    try:
        if len(df) > 0:

            df['calculo_wma'] = 2*ta.stream_WMA(df.close, periodo/2) - ta.stream_WMA(df.close, periodo)
            hma = ta.stream_WMA(df['calculo_wma'], math.floor(math.sqrt(periodo)))
            return hma
        else:
            print('No hay datos para calcular')
    except Exception as e:
        print('ERROR', e)

