from binance.client import Client
import config


try:
    cliente = Client(api_key=config.API_KEY, api_secret=config.API_SECRET)
    #se conectar con la api de binance
    print('Conexion Exitosa')
except Exception as e:
    print('EROOR: ', e)
    cliente = None