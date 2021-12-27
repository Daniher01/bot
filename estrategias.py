from indicadores import *
import funciones

def cruce_hma(df, periodo_mayor, periodo_menor): #estrategia solo para opciones BUY
    try:
        precio_actual = float(df['close'][-1:])
        vela_anterior = float(df['close'][-2:-1])
        dos_velas_antes = float(df['close'][-3:-2])
        hma80 = HMA(df, periodo_mayor)
        hma80 = hma80 + (hma80*0.022) #acercar lo mas posible al valor debido a la variacion
        hma50 = HMA(df, periodo_menor)
        hma50 = hma50 + (hma50*0.0053)
        #ejecutar opcion de compra
        if hma80 > hma50 and precio_actual > hma80:
            print('Cruce medias moviles')
            print('HMA80: ', hma80)
            print('HMA50: ', hma50)
            market = None
            if dos_velas_antes > hma80 and vela_anterior < precio_actual and dos_velas_antes < precio_actual:
                print('Oportunidad de compra')
                precio_compra = precio_actual
                market = True
                if hma50 > hma80 and vela_anterior < hma50 and market == True:
                    print('Cerrar Operacion')
                    precio_cierre = precio_actual
                    diferencia = precio_cierre - precio_compra
                    print('G/P en operacion: ', diferencia)
                    market = False
        else:
            print('No se esta cumpliendo la estrategia')
            market = None

    except Exception as e:
        market = None
        print('ERROR: ', e)
    return market
    #retorna booleano


