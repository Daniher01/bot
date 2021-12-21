import pandas as pd
import talib as ta
import numpy as np

import funciones
import indicadores

datos = funciones.datos_ticker('BTCUSDT', '1d', 'enero 2021')


contador = 0
lista = []
for i in datos.close:
    contador += 1
    lista.append(i)
    if contador >= 50:
        df = pd.DataFrame(lista)
        df['close'] = df[0]
        d = indicadores.HMA(df, 50)
        print(d)


