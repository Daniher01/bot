from indicadores import *

def cruce_hma(df, periodo1, periodo2):
    precio_actual = float(df['close'][-1:])
    vela_anterior = float(df['close'][-2:-1])
    dos_velas_antes = float(df['close'][-3:-2])
    hma50 = HMA(df, periodo1)
    hma80 = HMA(df, periodo2)
    if hma80 > hma50 and dos_velas_antes > hma80 and dos_velas_antes > vela_anterior and vela_anterior > precio_actual:
        print('se esta cumpliendo la estrategia')
        return True
    else:
        print('NO se esta cumpliendo la estrategia')
        return False




