import psycopg2
from binance.client import Client
import config



"""INSTANCIA API DE BINANCE"""
def binanceConnect():
    try:
        cliente = Client(api_key=config.API_KEY, api_secret=config.API_SECRET)
        #se conectar con la api de binance
        print('Conexion a binance Exitosa')
        return cliente
    except Exception as e:
        mensaje = 'EROOR AL CONECTAR CON BINANCE: ', e
        print(mensaje)
        cliente = None
        return cliente

def bdConnect():
    try:
        bd = psycopg2.connect(host=config.HOST, database=config.DBNAME, user=config.USER, password=config.PASSWORD)
        print('Conexion a la BD exitosa')
        return bd
    except Exception as e:
        mensaje = 'ERROR AL CONECTAR A LA BD: ', e
        print(mensaje)
        bd = None
        return  bd