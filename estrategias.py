from indicadores import *
import funciones

def cruce_hma(df, periodo1, periodo2):
    precio_actual = float(df['close'][-1:])
    vela_anterior = float(df['close'][-2:-1])
    dos_velas_antes = float(df['close'][-3:-2])
    hma50 = HMA(df, periodo1)
    hma80 = HMA(df, periodo2)
    if hma80 > hma50 and dos_velas_antes > hma80 and dos_velas_antes > vela_anterior and vela_anterior > precio_actual:
        print('Opcion de entrada')
        return True
    elif  hma50 > hma80 and precio_actual < hma50:
        print('Opcion de salida')
        return False
    else:
        print('No se esta cumpliendo la estrategia')
        return None

#data = funciones.datos_ticker('BTCUSDT', '1d', 'oct')
#d = cruce_hma(data,50,80)
