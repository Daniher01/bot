from binance.client import Client
import telebot
import config
from telegram.ext import Updater

"""INSTANCIA API DE BINANCE"""
try:
    cliente = Client(api_key=config.API_KEY, api_secret=config.API_SECRET)
    #se conectar con la api de binance
    print('Conexion Exitosa')
except Exception as e:
    print('EROOR: ', e)
    cliente = None

"""INSTANCIA API DE TELEGRAM"""
try:
    #tl = Updater(token=config.TOKEN, use_context=True)
    tl = telebot.TeleBot(config.TOKEN)
    print('Conexion con Telegram Exitosa')
except Exception as e:
    print('EROOR: ', e)
    tl = None