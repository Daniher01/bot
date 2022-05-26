from telegram.ext import Updater
import config
import funciones
from datetime import datetime

class ChatTelegram():

    def __init__(self, mensaje):
        #DATOS DEL SERVIDOR
        old, fechaActual = funciones.tiempo_server()
        #DATOS PARA EL MENSAJE
        html = f'<b>-Hora Servidor: </b> <u>{fechaActual}</u>\n' \
               f'<b>-Mensaje del Bot: </b>\n' \
               f' <i>{mensaje}</i>'
        updater = Updater(config.TOKEN, use_context=True)
        updater.bot.send_message(config.CHAT_ID,html,parse_mode = "HTML")