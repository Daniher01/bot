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
                if self.datadf['close'][dia] > vela_anterior and self.datadf['close'][dia] > dos_Velas_antes:
                    #if condicion != 1:
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

class Estrategia2_Acumular():
    #algoritmo para saber baktesting de estrategia HMA

    def __init__(self, cripto, time, limite=False):
        self.cripto = cripto
        self.time = time
        self.limite = limite
        self.datadf = funciones.datos_ticker(self.cripto, self.time, self.limite) #trae los ultimos 80 dias
        self.dolares = 100
        self.btc = 0
        self.precio_compra = 0
        self.precio_bajista = 0
        self.alcista = False
        """Valores por defecto"""
        self.HMA_1 = 50
        self.HMA_2 = 80
        self.HMA_3 = 200
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


    """Si el precio de venta es menor al precio de compra, no vende, sigue acumulando"""

    def senial_2(self):
        compra = []
        venta = []
        diferencia = []
        condicion = 0
        hma50 = self.bt_hma(self.HMA_1)
        hma80 = self.bt_hma(self.HMA_2)
        hma200 = self.bt_hma(self.HMA_3)
        self.datadf['hma50'] = hma50[0]
        self.datadf['hma80'] = hma80[0]
        self.datadf['hma200'] = hma200[0]
        for dia in range(len(self.datadf)):
            if dia > 1:
                vela_anterior = float(self.datadf['close'][dia - 1:dia])
                dos_Velas_antes = float(self.datadf['close'][dia - 2:dia - 1])
                precio_dia = float(self.datadf['close'][dia])
                # TENDENCIA ALCISTA
            if self.datadf['hma50'][dia] > self.datadf['hma80'][dia] and self.datadf['hma80'][dia] > self.datadf['hma200'][dia]:
                if condicion != 1 and self.alcista != True:
                    compra.append(self.datadf['close'][dia])
                    venta.append(np.nan)
                    diferencia.append(np.nan)
                    condicion = 1
                    precio_compra = self.datadf['close'][dia]
                    btc = self.dolares / precio_compra
                else:
                    compra.append(np.nan)
                    venta.append(np.nan)
                    diferencia.append(np.nan)
                self.alcista = True
                #TENDENCIA MERCADO BAJISTA
            elif self.datadf['hma80'][dia] > self.datadf['hma200'][dia] and self.datadf['hma50'][dia] > self.datadf['hma200'][dia]:
                if self.datadf['close'][dia] < vela_anterior  and dos_Velas_antes < self.datadf['hma200'][dia]:
                    if condicion != -1 and self.alcista == True:
                        venta.append(self.datadf['close'][dia])
                        compra.append(np.nan)
                        #diferencia.append(np.nan)
                        condicion = -1
                        porcentaje_gp = self.g_p(self.datadf['close'][dia], precio_compra, btc)
                        diferencia.append(porcentaje_gp)
                    else:
                        compra.append(np.nan)
                        venta.append(np.nan)
                        diferencia.append(np.nan)
                    self.alcista = False
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
        plt.plot(self.datadf['hma200'], label='HMA 200')
        plt.scatter(self.datadf.index, self.datadf['compra'], label='Precio de compra', marker='^', color='black')
        plt.scatter(self.datadf.index, self.datadf['venta'], label='Precio de venta', marker='v', color='red')
        plt.xlabel('Enero 2021 - Diciembre 2021')
        plt.ylabel('Precio cierra ($)')
        plt.legend(loc='upper left')
        plt.show()
        print('La relacion G/P en porcentaje para ', self.cripto, ' es: ', self.datadf['%'].sum(), '%')
        porcentaje = self.datadf['%'].sum()
        return self.datadf, porcentaje

"""----------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------"""
class Estrategia_compraDIP(): ##clase para la estrategia de bt

    def __init__(self,cripto, time, limite=False):
        self.cripto = cripto
        self.time = time
        self.limite = limite
        self.datadf = funciones.datos_ticker(cripto, time, limite)
        self.ATH = 0
        self.precioDIP = 0
        self.historial_ath = []
        self.DIP20percent = []

    #obtiene la ath de la cripto
    def ATH_bt(self):
        for dia in range(len(self.datadf)):
            precio_dia = float(self.datadf['close'][dia])
            if precio_dia > self.ATH:
                self.ATH = precio_dia
                self.historial_ath.append(self.ATH)
            else:
                self.historial_ath.append(np.nan)
        self.datadf['ATH'] = self.historial_ath
        return self.datadf #retorna el dataframe con una columna de todos los ath en el periodo dado

    #recibe el porcentaje en el que tiene que bajar el precio desde su ATH para hacer la compra
    def detectarPorcentajedeBajada(self, porcentaje):
        porcentaje = porcentaje/100
        precioDIP =self.ATH - (self.ATH * porcentaje)
        return  precioDIP

    def comprarDIP(self):
        self.ATH_bt()
        for dia in range(len(self.datadf)):
            precio_dia = float(self.datadf['close'][dia])
            #self.ATH = float(self.datadf['ATH'][dia])
            self.precioDIP = self.detectarPorcentajedeBajada(20)
            rango_diferancia = self.detectarPorcentajedeBajada( 21)
            if precio_dia <= self.precioDIP and precio_dia >= rango_diferancia:
                self.precioDIP = precio_dia
                self.DIP20percent.append(self.precioDIP)
            else:
                self.DIP20percent.append(np.nan)
            print('ATH ', self.ATH)
            print('DIP ',self.precioDIP)
            print('precio dia ', precio_dia)
            print('DIFERENCIA ',rango_diferancia)
        self.datadf['-20%'] = self.DIP20percent
        print(self.datadf)
        return self.datadf  # retorna el dataframe con una columna de todos los ath en el periodo dado


 #muestra el grafico
    def mostar_grafico(self):
        self.comprarDIP()
        plt.Figure(figsize=(10, 5))
        plt.plot(self.datadf['close'], label=self.cripto)

        plt.scatter(self.datadf.index, self.datadf['ATH'], label='ATH', marker='^', color='black')
        plt.scatter(self.datadf.index, self.datadf['-20%'], label='-20%', marker='v', color='red')
        plt.xlabel('FECHA')
        plt.ylabel('Precio cierra ($)')
        plt.legend(loc='upper left')
        plt.show()

        return self.datadf


d = Estrategia_compraDIP('BTCUSDT', '1d', 200)
d.mostar_grafico()







