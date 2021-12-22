import estrategias
import funciones

datos = funciones.datos_ticker('BTCUSDT', '1d', 'marzo 2021')
estrategias.cruce_hma(datos, 80,50)











