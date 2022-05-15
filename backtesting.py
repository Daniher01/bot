import numpy
import pandas as pd
import numpy as np
from conexion import bdConnect
import funciones
import matplotlib.pyplot as plt

"""
Clase para realizar los backtesting manualmente
"""

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
        self.btc_acumulado = 0
        self.dolares = 60
        self.liquidez_invertida = 0
        self.precio_bajada = 0
        self.lista_precioCompra = []
        self.preciosDIP = []
        self.historial_ath = []
        self.hayATH = []
        self.lista_porcentaje = [10,20,30,40,50]
        self.DIP5 = []
        self.DIP10 = []
        self.DIP20 = []
        self.DIP30 = []
        self.DIP40 = []
        self.DIP50 = []



    #recibe el porcentaje en el que tiene que bajar el precio desde su ATH para hacer la compra
    def detectarPorcentajedeBajada(self, porcentaje):
        porcentaje = porcentaje/100
        porcentaje_diferencia = porcentaje+1/100
        precioDIP =self.ATH - (self.ATH * porcentaje)
        rango_diferencia = self.ATH - (self.ATH * porcentaje_diferencia)

        return precioDIP

    #permite saber cuanto btc se va acumulando con cada compra
    def saber_btc_acumulado(self, precio_btc):
        self.btc_acumulado += (self.dolares / precio_btc)
        self.liquidez_invertida += self.dolares



    def comprarDIP(self):
        self.preciosDIP = []

        for dia in range(len(self.datadf)):
            precio_dia = float(self.datadf['close'][dia])


            self.sePuedeComprar = False
            """Se obtiene el ATH de la cripto"""
            if precio_dia > self.ATH: #cambiar ath por el precio dia
                self.ATH = precio_dia
                self.historial_ath.append(self.ATH)
                self.hayATH.append(True)
                lista = [5,10,15,20,25,30,35,40,45,50]
                self.lista_precioDip = []


                print('ATH: ', self.ATH)
                for dip in lista:
                    self.precioDIP = self.detectarPorcentajedeBajada(dip)
                    self.lista_precioDip.append(self.precioDIP)

            else:
                self.historial_ath.append(np.nan)
                self.hayATH.append(False)


            print(self.lista_precioDip)

            for precioDIP in self.lista_precioDip:
                print(self.lista_precioDip[-1])
                rango_diferencia = precioDIP - (precioDIP*0.01)
                if precio_dia <= precioDIP and precio_dia >= rango_diferencia:
                    self.lista_precioCompra.append(precio_dia)
                    if precioDIP == self.lista_precioDip[-1]:
                        print('HOLA')
                    #self.lista_precioDip.remove(precioDIP)



            if len(self.lista_precioCompra) > 0:
                for i in self.lista_precioCompra:
                    if i > 1:
                        self.preciosDIP.append(i)
                    else:
                        self.preciosDIP.append(np.nan)
            else:
                self.preciosDIP.append(np.nan)

            self.lista_precioCompra = []


            """if self.contador == 10:
                self.precioDIP, rango_diferencia = self.detectarPorcentajedeBajada(self.contador)
                if precio_dia <= self.precioDIP and precio_dia >= rango_diferencia:
                    self.precioDIP = precio_dia
                    self.DIP10.append(self.precioDIP)
                    self.sePuedeComprar = True
                else:
                    self.DIP10.append(np.nan)
                self.contador +=10


            if self.contador == 20:
                self.precioDIP, rango_diferencia = self.detectarPorcentajedeBajada(self.contador)
                if precio_dia <= self.precioDIP and precio_dia >= rango_diferencia:
                    self.precioDIP = precio_dia
                    self.DIP20.append(self.precioDIP)
                    self.sePuedeComprar = True
                else:
                    self.DIP20.append(np.nan)
                self.contador +=10


            if self.contador == 30:
                self.precioDIP, rango_diferencia = self.detectarPorcentajedeBajada(self.contador)
                if precio_dia <= self.precioDIP and precio_dia >= rango_diferencia:
                    self.precioDIP = precio_dia
                    self.DIP30.append(self.precioDIP)
                    self.sePuedeComprar = True
                else:
                    self.DIP30.append(np.nan)
                self.contador +=10


            if self.contador == 40:
                self.precioDIP, rango_diferencia = self.detectarPorcentajedeBajada(self.contador)
                if precio_dia <= self.precioDIP and precio_dia >= rango_diferencia:
                    self.precioDIP = precio_dia
                    self.DIP40.append(self.precioDIP)
                    self.sePuedeComprar = True
                else:
                    self.DIP40.append(np.nan)
                self.contador +=10


            if self.contador == 50:
                self.precioDIP, rango_diferencia = self.detectarPorcentajedeBajada(self.contador)
                if precio_dia <= self.precioDIP and precio_dia >= rango_diferencia:
                    self.precioDIP = precio_dia
                    self.DIP50.append(self.precioDIP)
                    self.sePuedeComprar = True
                else:
                    self.DIP50.append(np.nan)

                self.contador = 10


            if self.sePuedeComprar == True:
                self.saber_btc_acumulado(precio_dia)
                self.promedio_compra.append(precio_dia)

            self.sePuedeComprar = False



        self.datadf['ATH'] = self.historial_ath

        self.datadf['-10%'] = self.DIP10
        self.datadf['-20%'] = self.DIP20
        self.datadf['-30%'] = self.DIP30
        self.datadf['-40%'] = self.DIP40
        self.datadf['-50%'] = self.DIP50


        promedio = numpy.mean(self.promedio_compra)
        print(promedio)
        lista = ['BTC acumulado: ',self.btc_acumulado, 'total invertido en $$: ',self.liquidez_invertida, 'Promedio de compra: ',promedio]
        lista_df = pd.DataFrame(lista)
        lista_df.to_csv('resumen comprar en el DIP.csv')"""
        self.datadf['ATH'] = self.historial_ath
        print(len(self.preciosDIP))
        self.datadf['-%'] = self.preciosDIP
        #print(self.datadf)
        return self.datadf  # retorna el dataframe con una columna de todos los ath en el periodo dado


    def compras_progresivas(self):
        contador = 0
        for dia in range(len(self.datadf)):
            precio_dia = float(self.datadf['close'][dia])
            contador += 1

            if contador == 7:
                contador = 0
                self.saber_btc_acumulado(precio_dia)
                self.promedio_compra.append(precio_dia)
            else:
                self.promedio_compra.append(np.nan)


        promedio = numpy.mean(self.promedio_compra)

        self.datadf['DCA'] = self.promedio_compra
        lista = ['BTC acumulado: ', self.btc_acumulado, 'total invertido en $$: ', self.liquidez_invertida]
        lista_df = pd.DataFrame(lista)
        lista_df.to_csv('resumen compras progresivas.csv')


 #muestra el grafico
    def mostar_grafico(self):
        self.comprarDIP()
        #self.compras_progresivas()
        plt.Figure(figsize=(10, 5))
        plt.plot(self.datadf['close'], label=self.cripto)

        #plt.scatter(self.datadf.index, self.datadf['DCA'], label='DCA', marker='o', color='black')

        plt.scatter(self.datadf.index, self.datadf['ATH'], label='ATH', marker='o', color='black')
        plt.scatter(self.datadf.index, self.datadf['-%'], label='-%', marker='v', color='red')

        """plt.scatter(self.datadf.index, self.datadf['-10%'], label='-10%', marker='v', color='red')
        plt.scatter(self.datadf.index, self.datadf['-20%'], label='-20%', marker='v', color='blue')
        plt.scatter(self.datadf.index, self.datadf['-30%'], label='-30%', marker='v', color='brown')
        plt.scatter(self.datadf.index, self.datadf['-40%'], label='-40%', marker='v', color='purple')
        plt.scatter(self.datadf.index, self.datadf['-50%'], label='-50%', marker='v', color='orange')"""


        plt.xlabel('FECHA')
        plt.ylabel('Precio cierra ($)')
        plt.legend(loc='upper left')
        plt.show()

        return self.datadf


d = Estrategia_compraDIP('BTCUSDT', '1d', 365)
d.mostar_grafico()
#d.comprarDIP()
#d.compras_progresivas()






