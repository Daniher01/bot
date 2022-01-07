import time
from os import path, remove
from datetime import datetime
from telegram.ext import Updater, CommandHandler
import conexion
import config
from estrategias import *
import funciones
import requests
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
        self.mensaje = None
        self.tradingView_pag = 'https://WWW.tradingview.com/chart/UBCV9gCj/?symbol='
        self.binance_pag = 'https://www.binance.com/es/trade/'
        """Se le asigna el tiempo del servidor"""
        self.seconds = 0
        self.minute = 0
        self.hour = 0

    def log(self, cripto, precio_compra):
        """Resgistro de actividad del bot"""
        old, new = funciones.tiempo_server()
        lista_registro = [[cripto], [precio_compra], [new]]
        registro_df = pd.DataFrame(lista_registro)
        if not path.exists('%s-%s-data.csv' % (cripto, self.descripcion)):
            funciones.get_csv(registro_df, cripto, self.descripcion)
        pass

    #mostrar la lista de cripto
    def get_list_cripto(self,update, context):
        update.message.reply_text(f'Lista de criptomonedas para la estrategia')
        for cripto in self.lista_cripto:
            update.message.reply_text(cripto)
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
        if path.exists('%s-%s-data.csv' % (cripto, self.descripcion)): #para la venta
            print('Leyendo el precio de compra')
            registros_df = funciones.leer_csv(cripto, self.descripcion) #se lee el precion de compra
            precio_compra = registros_df[1][2]
            #estrategias.sell(precio_compra)
            remove('%s-%s-data.csv' % (cripto, self.descripcion)) #se lee el precio y elimina el archivo
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
        self.accion = self.estrategia(cripto)
        if self.accion == 2:
            aviso=f'Cruce medias moviles \n HMA80: {self.HMA_L} \n HMA50: {self.HMA_C}'
        elif self.accion == 1:
            aviso='Oportunidad de compra'
            self.log(cripto, self.precio_compra)
        elif self.accion == -2:
            aviso='Cierra 50%'
        elif self.accion == -1:
            aviso='cierra todo'
        else:
            aviso='No hay entradas ni salidas'
        moneda = self.buscar_moneda(cripto)
        if moneda == cripto:
            moneda_tiene='Ya tienes esa moneda'
        else:
            moneda_tiene='No tienes esa moneda'
        self.mensaje = (f'{cripto} \n {aviso} \n {moneda_tiene}')
        return self.mensaje

    def start(self,update, context): #automatizar el solo mostrar la estrategia
        try:
            updater = Updater(config.TOKEN, use_context=True)
            updater.bot.send_message(config.CHAT_ID, 'Corriendo bot...')
            while self.RUN:
                self.tiempo()
                for i in self.lista_cripto:
                    updater.bot.send_message(config.CHAT_ID, self.avisar(i))
                    if self.accion == 2 and self.hour == 00:
                        updater.bot.send_message(config.CHAT_ID, 'Puedes Ejecutar Ordenes...')
                        updater.bot.send_message(config.CHAT_ID, f'Pagina TradingView: \n {self.tradingView_pag}{i}')
                        updater.bot.send_message(config.CHAT_ID, f'Pagina Binance: \n {self.binance_pag}{i}')
                    else:
                        old, new = funciones.tiempo_server()
                        updater.bot.send_message(config.CHAT_ID,
                                                 f'Se recomienda esperar a que sean las 12 hora del servidor... \n {new}')
                time.sleep((60*60)*4) #cada 4 horas se va a ejecutar
        except Exception as e:
            updater.bot.send_message(config.CHAT_ID, f'ERROR: \n {e}')
            print('ERROR: ',e)


    def run(self):
        try:
            # ejecuta en telegram
            updater = Updater(config.TOKEN, use_context=True)
            updater.dispatcher.add_handler(CommandHandler('start', self.start))

            # start
            updater.start_polling()
            print('listo para utilizar')


            # me quedo esperando
            updater.idle()
        except Exception as e:
            updater.bot.send_message(config.CHAT_ID, f'ERROR: \n {e}')
            print('ERROR: ', e)


bot = CriptoBot() #instancia el bot
bot.run()



