from datetime import datetime
import time
import conexion
import estrategias
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
        self.sellsignal = False
        self.buysignal = False
        self.orden_status = None
        self.orden = None
        self.RUN = True
        self.seconds = 0
        self.minute = 0
        self.hour = 0

    def log(self):
        """Resgistro de actividad del bot"""
        pass

    def estrategia(self):
        """elegir estrategia"""
        cumple = estrategias.cruce_hma(self.data_df, self.HMA_L, self.HMA_C)
        return cumple

    def cripto(self, cripto):
        self.data_df = funciones.datos_ticker(cripto, self.time, self.limite)
        print(cripto)
        self.estrategia()
        pass

    def tiempo(self):
        time_res = conexion.cliente.get_server_time()
        ts = time_res.get('serverTime')
        self.seconds = datetime.utcfromtimestamp(ts / 1000).second
        self.minute = datetime.utcfromtimestamp(ts / 1000).minute
        self.hour = datetime.utcfromtimestamp(ts / 1000).hour
        pass

    def avisar(self):
        """venta, comrpra, resumen llamado al metodo log"""
        #avisar mediante telegram
        for i in self.lista_cripto:
            self.data_df = funciones.datos_ticker(i, self.time, self.limite)
            print(i)
            self.estrategia()
            balance = funciones.balance()
            for d in range(len(balance)):
                if balance['asset'][d] + 'USDT' == i:
                    print('Ya tienes esa moneda')
            print('')
        return self.data_df

    def run(self):
        while self.RUN:
            try:
                self.tiempo()
                """CUANDO SEAN LAS 23:55 EN HORA DEL SERVIDOR"""
                if self.hour == 23 and self.minute == 55:
                    funciones.tiempo_server()
                    self.avisar()
            except Exception as e:
                print('ERROR: ',e)
                self.RUN = False
  
d = funciones.balance()
print(d)



#TODO tiempo de espera, una vez al dia
