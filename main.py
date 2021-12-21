import matplotlib.pyplot as plt
import funciones
import backtesting
import pandas as pd

import indicadores

datos = funciones.datos_ticker('BTCUSDT', '1d', 'enero 2021')

wma50 = backtesting.bt_wma(datos, 50)
wma80 = backtesting.bt_wma(datos, 80)

hma80 = backtesting.bt_hma(datos,80)
hma50 = backtesting.bt_hma(datos,50)




plt.Figure(figsize=(10,5))
plt.plot(datos['close'], label = 'Bitcoin')
plt.plot(hma50[0], label = 'WMA 50')
plt.plot(hma80[0], label = 'WMA 80')
plt.title('Media Movil Ponderada Bitcoin')
plt.xlabel('Enero 2021 - Diciembre 2021')
plt.ylabel('Precio cierra ($)')
plt.legend(loc = 'upper left')
plt.show()


