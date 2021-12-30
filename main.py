import os.path
import time
from datetime import datetime
#import bot_tl
import pandas as pd

import conexion
from estrategias import *
import funciones
#import backtesting

class CriptoBot():
    def __init__(self):
        self.cliente = conexion.cliente
        self.lista_cripto = ['BTCUSDT', 'SOLUSDT', 'DOTUSDT', 'LUNAUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT']
        self.time = '1d'
        self.limite = 80
        self.data_df = ''
        """Valores por defecto"""
        self.HMA_L = 80
        self.HMA_C = 50
        self.RUN = True
        self.accion = 0 #1 esta en compra, -1 esta en venta
        self.precio_compra = 0 #guardar el precio al momento de hacer la compra
        self.descripcion = 'Registro_compra' #descripcion para el nombre del csv
        self.seconds = 0
        self.minute = 0
        self.hour = 0

    def log(self, cripto, precio_compra):
        """Resgistro de actividad del bot"""
        old, new = funciones.tiempo_server()
        lista_registro = [[cripto], [precio_compra], [new]]
        registro_df = pd.DataFrame(lista_registro)
        funciones.get_csv(registro_df, cripto, self.descripcion)
        pass

    def buscar_moneda(self, cripto):
        balance = funciones.balance()
        for d in range(len(balance)):
            if balance['asset'][d] + 'USDT' == cripto:
                return cripto

    def estrategia(self, cripto):
        """elegir estrategia"""
        estrategias = Cruce_hma(self.data_df, self.HMA_L, self.HMA_C)
        self.precio_compra = estrategias.buy() #precion de compra
        if os.path.exists('%s-%s-data.csv' % (cripto, self.descripcion)):
            print('HOLA')
            registros_df = funciones.leer_csv(cripto, self.descripcion) #se lee el precion de compra
            precio_compra = registros_df[1][2]
            estrategias.sell(precio_compra)
        cumple = estrategias.market
        return cumple

    def tiempo(self):
        time_res = conexion.cliente.get_server_time()
        ts = time_res.get('serverTime')
        self.seconds = datetime.utcfromtimestamp(ts / 1000).second
        self.minute = datetime.utcfromtimestamp(ts / 1000).minute
        self.hour = datetime.utcfromtimestamp(ts / 1000).hour
        pass


    def avisar(self, cripto):
        self.data_df = funciones.datos_ticker(cripto, self.time, self.limite)
        print(cripto)
        self.accion = self.estrategia(cripto)
        if self.accion == 2:
            print('cruce medias moviles')
        elif self.accion == 1:
            print('oportunidad de compra')
            self.log(cripto, self.precio_compra)
        elif self.accion == -2:
            print('cierra 50 porciento')
        elif self.accion == -1:
            print('cierra todo')
        else:
            print('no hay entradas ni salidas')
        moneda = self.buscar_moneda(cripto)
        if moneda == cripto:
            print('Ya tienes esa moneda')
        print('')

    def run(self):
        while self.RUN:
            try:
                self.tiempo()
                """CUANDO SEAN LAS 23:55 EN HORA DEL SERVIDOR"""
                if self.hour == 23 and self.minute == 55:
                    funciones.tiempo_server()
                    for i in self.lista_cripto:
                        self.avisa(i)
            except Exception as e:
                print('ERROR: ',e)
                self.RUN = False
  

""""@conexion.tl.message_handler(commands=['start', 'help'])
def send_welcome(message, msj='Mensaje de prueba'):
    conexion.tl.reply_to(message, msj)

@conexion.tl.message_handler(func=lambda message: True)
def echo_all(message):
    conexion.tl.reply_to(message, message.text)

conexion.tl.polling()"""


bot = CriptoBot()
for i in bot.lista_cripto:
    bot.avisar(i)


