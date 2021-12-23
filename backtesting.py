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
class Estrategia1_ST():
    #algoritmo para saber baktesting de estrategia HMA
    def senial_hma(self, data, dolares):
        compra = []
        venta = []
        diferencia = []
        condicion = 0
        for dia in range(len(data)):
            if dia > 1:
                vela_anterior = float(data['close'][dia-1:dia])
                dos_Velas_antes = float(data['close'][dia-2:dia-1])
                #AL MOMENTO DE COMPRAR
            if data['hma80'][dia] > data['hma50'][dia] and dos_Velas_antes > data['hma80'][dia]:
                if data['close'][dia] > vela_anterior and data['close'][dia] > dos_Velas_antes:
                    if condicion != 1:
                        compra.append(data['close'][dia])
                        venta.append(np.nan)
                        diferencia.append(np.nan)
                        precio_compra = data['close'][dia]
                        btc = dolares / precio_compra
                        condicion = 1
                    else:
                        compra.append(np.nan)
                        venta.append(np.nan)
                        diferencia.append(np.nan)
                else:
                    compra.append(np.nan)
                    venta.append(np.nan)
                    diferencia.append(np.nan)
                    #AL MOMENTO DE VENDER
            elif data['hma80'][dia] < data['hma50'][dia] and data['close'][dia] < data['hma50'][dia] and condicion == 1:
                if condicion != -1:
                    venta.append(data['close'][dia])
                    compra.append(np.nan)
                    g_p = (data['close'][dia] - precio_compra) * btc * 1 #calculo ganancia perdida
                    porcentaje_gp = (g_p*100)/dolares #g/p en porcentaje
                    diferencia.append(porcentaje_gp)
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



    def bt_wma(self, df, periodo):
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

    def bt_hma(self, df, periodo):
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



datos = funciones.datos_ticker('DOTUSDT', '1d',80)
est1 = Estrategia1_ST() #se instancia la clase
hma50 = est1.bt_hma(datos,50)
hma80 = est1.bt_hma(datos,80)

datos['hma50'] = hma50[0]
datos['hma80'] = hma80[0]

compra, venta, diferencia = est1.senial_hma(datos, 50)
datos['compra'] = compra
datos['venta'] = venta
datos['%'] = diferencia

print('La relacion G/P en porcentaje es: ',datos['%'].sum(),'%')

funciones.get_csv(datos, 'DOTUSDT', '1d') #se genera el csv

plt.Figure(figsize=(10,5))
plt.plot(datos['close'], label = 'Bitcoin')
plt.plot(datos['hma50'], label = 'HMA 50')
plt.plot(datos['hma80'], label = 'HMA 80')
plt.scatter(datos.index, datos['compra'], label ='Precio de compra', marker='^', color='black')
plt.scatter(datos.index, datos['venta'], label ='Precio de venta', marker='v', color='red')
plt.xlabel('Enero 2021 - Diciembre 2021')
plt.ylabel('Precio cierra ($)')
plt.legend(loc = 'upper left')
plt.show()

