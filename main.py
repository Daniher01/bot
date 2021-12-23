from binance.exceptions import BinanceAPIException, BinanceOrderException
import conexion
import estrategias


class CriptoBot():
    def __init__(self, cripto, time, data_df):
        self.cliente = conexion.cliente
        self.cripto = cripto
        self.time = time #temporalidad
        self.data_df = data_df

    def log(self):
        """Resgistro de actividad del bot"""
        pass

    def last_data(self):
        """actualizar datos necesarios para la toma de decisiones"""
        pass

    def estrategia(self):
        """elegir estrategia"""
        pass

    def order(self):
        """venta, comrpra, resumen llamado al metodo log"""
        pass


