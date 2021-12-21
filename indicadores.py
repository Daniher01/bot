import math

import numpy as np
import pandas as pd
import talib as ta
"""
Se tienen funciones de los indicadores 
que no estan en la libreria TA-Lib

"""

def HMA(df, periodo):
    try:
        if len(df) > 0:
            #calculo de la Media Movil de Hull
            df['hma'] = 2 * ta.stream_WMA(df.close, periodo / 2) - ta.stream_WMA(df.close, periodo)
            hma = ta.stream_WMA(df['hma'], math.floor(math.sqrt(periodo)))
            return hma
        else:
            print('No hay datos para calcular')
            return None
    except Exception as e:
        print('ERROR', e)

