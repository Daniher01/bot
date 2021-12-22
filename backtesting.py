import pandas as pd
import numpy as np
import talib as ta

import estrategias
import indicadores
import funciones
import matplotlib.pyplot as plt

"""
Clase para realizar los backtesting manualmente
"""

#algoritmo para saber bt de estrategia HMA
def senial_hma(data):
    compra = []
    venta = []
    diferencia = []
    condicion = 0
    for dia in range(len(data)):
        if dia > 1:
            vela_anterior = float(data['close'][dia-1:dia])
            dos_Velas_antes = float(data['close'][dia-2:dia-1])
        if data['hma80'][dia] > data['hma50'][dia] and dos_Velas_antes > data['hma80'][dia]:
            if data['close'][dia] > vela_anterior and data['close'][dia] > dos_Velas_antes:
                if condicion != 1:
                    compra.append(data['close'][dia])
                    venta.append(np.nan)
                    diferencia.append(np.nan)
                    precio_compra = data['close'][dia]
                    condicion = 1
                else:
                    compra.append(np.nan)
                    venta.append(np.nan)
                    diferencia.append(np.nan)
            else:
                compra.append(np.nan)
                venta.append(np.nan)
                diferencia.append(np.nan)
        elif data['hma80'][dia] < data['hma50'][dia] and data['close'][dia] < data['hma50'][dia] and condicion == 1:
            if condicion != -1:
                venta.append(data['close'][dia])
                compra.append(np.nan)
                dif = precio_compra - data['close'][dia]
                diferencia.append(dif)
                condicion = -1
            else:
                compra.append(np.nan)
                venta.append(np.nan)
                diferencia.append(np.nan)
        else:
            compra.append(np.nan)
            venta.append(np.nan)
            diferencia.append(np.nan)

    return compra, venta, diferencia



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
    lista_wma = []  # lista para guardar las wma de los precios}
    for i in df.close:
        contador += 1
        lista_close.append(i)
        data = pd.DataFrame(lista_close)
        data['close'] = data[0]
        d = indicadores.HMA(data, periodo)
        lista_wma.append(d)
        data_df = pd.DataFrame(lista_wma)
    return data_df

datos = funciones.datos_ticker('BTCUSDT', '1d', 'enero 2021')

hma50 = bt_hma(datos,50)
hma80 = bt_hma(datos,80)

data = pd.DataFrame()
data['close'] = datos.close
data['hma50'] = hma50[0]
data['hma80'] = hma80[0]

compra, venta, diferencia = senial_hma(data)
data['compra'] = compra
data['venta'] = venta
data['diferencia'] = diferencia


plt.Figure(figsize=(10,5))
plt.plot(data['close'], label = 'Bitcoin')
plt.plot(data['hma50'], label = 'HMA 50')
plt.plot(data['hma80'], label = 'HMA 80')
plt.scatter(data.index, data['compra'], label ='Precio de compra', marker='^', color='black')
plt.scatter(data.index, data['venta'], label ='Precio de venta', marker='v', color='red')
plt.xlabel('Enero 2021 - Diciembre 2021')
plt.ylabel('Precio cierra ($)')
plt.legend(loc = 'upper left')
plt.show()

