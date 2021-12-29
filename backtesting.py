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

    def __init__(self, cripto, time, limite=False):
        self.cripto = cripto
        self.time = time
        self.limite = limite
        self.datadf = funciones.datos_ticker(self.cripto, self.time, self.limite) #trae los ultimos 80 dias
        self.dolares = 10
        """Valores por defecto"""
        self.HMA_L = 80
        self.HMA_C = 50
        self.op_compra = []


    def bt_hma(self, periodo):
        contador = 0
        lista_close = []  # lista para guardar precios de cierra
        lista_hma = []  # lista para guardar las hma de los precios
        for i in self.datadf.close:
            contador += 1
            lista_close.append(i)
            data = pd.DataFrame(lista_close)
            data['close'] = data[0]
            d = indicadores.HMA(data, periodo)
            lista_hma.append(d)
            data_df = pd.DataFrame(lista_hma)
        return data_df

    def g_p(self, p_cierre, p_compra, btc):
        g_p = (p_cierre - p_compra) * btc * 1  # calculo ganancia perdida
        porcentaje_gp = (g_p * 100) / self.dolares  # g/p en porcentaje
        return porcentaje_gp


    def senial_hma(self):
        compra = []
        venta = []
        diferencia = []
        condicion = 0
        hma50 = self.bt_hma(self.HMA_C)
        hma80 = self.bt_hma(self.HMA_L)
        self.datadf['hma50'] = hma50[0]
        self.datadf['hma80'] = hma80[0]
        for dia in range(len(self.datadf)):
            if dia > 1:
                vela_anterior = float(self.datadf['close'][dia - 1:dia])
                dos_Velas_antes = float(self.datadf['close'][dia - 2:dia - 1])
                # AL MOMENTO DE COMPRAR
            if self.datadf['hma80'][dia] > self.datadf['hma50'][dia] and dos_Velas_antes > self.datadf['hma80'][dia]:
                if self.datadf['close'][dia] > vela_anterior and dos_Velas_antes < self.datadf['close'][dia] :
                    if condicion != 1:
                        compra.append(self.datadf['close'][dia])
                        venta.append(np.nan)
                        diferencia.append(np.nan)
                        precio_compra = self.datadf['close'][dia]
                        btc = self.dolares / precio_compra
                        condicion = 1
                        self.op_compra.append(1)
                    else:
                        compra.append(np.nan)
                        venta.append(np.nan)
                        diferencia.append(np.nan)
                else:
                    compra.append(np.nan)
                    venta.append(np.nan)
                    diferencia.append(np.nan)
                    # AL MOMENTO DE VENDER
            elif self.datadf['hma80'][dia] < self.datadf['hma50'][dia] and self.datadf['close'][dia] < self.datadf['hma50'][
                dia] and condicion == 1:
                if condicion != -1:
                    venta.append(self.datadf['close'][dia])
                    compra.append(np.nan)
                    porcentaje_gp = self.g_p(self.datadf['close'][dia], precio_compra, btc)
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

        self.datadf['compra'] = compra
        self.datadf['venta'] = venta
        self.datadf['%'] = diferencia
        return self.datadf

    """Si el precio de venta es menor al precio de compra, no vende, sigue acumulando"""
    def senial_2(self):
        compra = []
        venta = []
        diferencia = []
        condicion = 0
        hma50 = self.bt_hma(self.HMA_C)
        hma80 = self.bt_hma(self.HMA_L)
        self.datadf['hma50'] = hma50[0]
        self.datadf['hma80'] = hma80[0]
        for dia in range(len(self.datadf)):
            if dia > 1:
                vela_anterior = float(self.datadf['close'][dia - 1:dia])
                dos_Velas_antes = float(self.datadf['close'][dia - 2:dia - 1])
                # AL MOMENTO DE COMPRAR
            if self.datadf['hma80'][dia] > self.datadf['hma50'][dia] and dos_Velas_antes > self.datadf['hma80'][dia]:
                if self.datadf['close'][dia] > vela_anterior and dos_Velas_antes < self.datadf['close'][dia]:
                    if condicion != 1:
                        compra.append(self.datadf['close'][dia])
                        venta.append(np.nan)
                        diferencia.append(np.nan)
                        precio_compra = self.datadf['close'][dia]
                        btc = self.dolares/ precio_compra
                        condicion = 1
                        self.op_compra.append(1)
                    else:
                        compra.append(np.nan)
                        venta.append(np.nan)
                        diferencia.append(np.nan)
                else:
                    compra.append(np.nan)
                    venta.append(np.nan)
                    diferencia.append(np.nan)
                    # AL MOMENTO DE VENDER
            elif self.datadf['hma80'][dia] < self.datadf['hma50'][dia] and vela_anterior < self.datadf['hma50'][dia] and self.datadf['close'][dia] < \
                    self.datadf['hma80'][dia] :
                if condicion == 1 and precio_compra < self.datadf['close'][dia]:
                    venta.append(self.datadf['close'][dia])
                    compra.append(np.nan)
                    porcentaje_gp = self.g_p(self.datadf['close'][dia], precio_compra, btc)
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

        self.datadf['compra'] = compra
        self.datadf['venta'] = venta
        self.datadf['%'] = diferencia
        return self.datadf


    def mostar_grafico(self):
        self.senial_2()
        plt.Figure(figsize=(10, 5))
        plt.plot(self.datadf['close'], label=self.cripto)
        plt.plot(self.datadf['hma50'], label='HMA 50')
        plt.plot(self.datadf['hma80'], label='HMA 80')
        plt.scatter(self.datadf.index, self.datadf['compra'], label='Precio de compra', marker='^', color='black')
        plt.scatter(self.datadf.index, self.datadf['venta'], label='Precio de venta', marker='v', color='red')
        plt.xlabel('Enero 2021 - Diciembre 2021')
        plt.ylabel('Precio cierra ($)')
        plt.legend(loc='upper left')
        plt.show()
        print('La relacion G/P en porcentaje para ', self.cripto, ' es: ', self.datadf['%'].sum(), '%')
        porcentaje = self.datadf['%'].sum()
        return self.datadf, porcentaje




lista_cripto = ['BTCUSDT', 'SOLUSDT', 'DOTUSDT', 'LUNAUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT']
lista = []
for i in lista_cripto:
    data = Estrategia1_ST(i, '1d', 365)
    print('')
    print(i)
    datos, porcentaje = data.mostar_grafico()
    lista.append(porcentaje)
    print(len(data.op_compra))
sum_portafolio = pd.DataFrame(lista)
print('la G/p del portafolio es: ',sum_portafolio.sum())


#funciones.get_csv(datos, 'BTCUSDT', '1d') #se genera el csv


