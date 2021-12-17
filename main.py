from indicadores import *

def cruce_hma(df, periodo1, periodo2):
    precio = float(df['close'][-1:])
    hma50 = HMA(df, periodo1)
    hma80 = HMA(df, periodo2)
    if hma80 > hma50 and precio > hma80:
        print('se esta cumpliendo la estrategia')
        return True
    else:
        print('NO se esta cumpliendo la estrategia')
        return False




