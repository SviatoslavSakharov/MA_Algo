import pandas as pd 
import numpy as np
import matplotlib.pyplot  as plt
from functions import get_ma_va


va = 20   #  volume avarage
ma = 90   # moving avarage (среднее значение цены за "ma" дней) 

data = pd.read_csv("price.csv", header = 1)  # read csv with header
data = data[::-1]   # reverse dataframe  ( просто в цсв файле все наоборот, сначала новые данные а в конце старые. чтобы потом легче делать for loop )
open_price = data['Open'].to_numpy()    # просто создаю array с открытием цены 
close_price = data['Close'].to_numpy()
volume = data['Volume BTC'].to_numpy()

start, ma_arr, va_arr = get_ma_va(close_price, volume, ma, va)  
open_price = open_price[start:]
close_price = close_price[start:]
volume = volume[start:]

stop_loss_prc = 0.01   # стоп лосс, если например после пересечение MA цена пошла в другую сторону медленно и не пересекает MA, указывается в процентах от цены
volume_prc = 0    # процент обьема с которым цена должна пересечь MA чтобы купить или продать. Вообще с ним выходит намного меньше денег, поэтому пока 0
usdt_prc = 0.5   # процент от кошелька за который покупать или продавать крипту. только для теста сейчас
usdt = 600   # начальный кошелек
usdt_arr = []   # сюда будет скидываться баланс кошелька после покупки->продажи или продажи->покупки
btc_old_price = 0 # прошлая цена биткоина во время которой была продажа или покупка
contract = 0  #  контракт в биткоинах, если купил то больше 0 если продал то меньше
action = '' # действия что мне надо ? купить или продать 

for i in range(1,len(close_price)):
    if usdt <= 0 or len(usdt_arr)==-1: # тупое бессмысленное if
        print('END')
        break

    if action == 'Sell' and  btc_old_price - btc_old_price*stop_loss_prc > close_price[i] and contract != 0 :   # стоп лосс если мне надо продать а цена пошла вниз
        usdt = usdt + contract*close_price[i]
        usdt_arr.append(usdt)
        contract = 0

    elif action == 'Buy' and  btc_old_price + btc_old_price*stop_loss_prc < close_price[i] and contract != 0 :   # стоп лосс если мне надо купить а цена пошла наверх
        usdt = usdt + contract*close_price[i]
        usdt_arr.append(usdt)
        contract = 0 


    if ( ma_arr[i-1]<close_price[i-1] and ma_arr[i-1]>open_price[i-1] and close_price[i]>ma_arr[i]):   # если прошлая свеча пересекла МА вверх и теперешняя цена не пересекла ее обратно в другую сторону (значит наверное тренд наверх и цена будет рости)
        if contract != 0 and action == 'Buy':   # имеет смысл если есть проценты по обьему но пока они 0
            #print('open price = ', open_price[i], ' close_price =', close_price[i])
            #print('Buy' )
            usdt = usdt + contract*close_price[i]
            usdt_arr.append(usdt)
            contract = 0
            #print('Contract = ', contract)
            #print('Usdt = ', usdt)
        if volume[i-1] > volume_prc*va_arr[i-1]: # так же меет смысл если есть проценты по обьему, сейчас работает всегда
            #print('open price = ', open_price[i], ' close_price =', close_price[i])
            
            # если контракта на продажу или покупку нет, значит надо купить контракт
            if contract == 0:   
                #print('Buy ')
                contract = usdt*usdt_prc/close_price[i]
                usdt = usdt - usdt*usdt_prc
                btc_old_price = close_price[i]
                #print('Contract = ', contract)
                #print('Usdt = ', usdt)
                action = 'Sell' # контракт надо потом продать 
                #print('I want to sell')

            # если контракт на покупку есть значит надо купить
            elif contract != 0 and action == 'Buy':
                #print('Buy ')
                usdt = usdt + contract*close_price[i]
                usdt_arr.append(usdt)
                contract = 0
                #print('Contract = ', contract)
                #print('Usdt = ', usdt)
            # если контракт на продажу значит лучше держать дальше, потому что цена растет
            else :
                pass
                #print('HODL')
    
    # все тоже самое только если прошлая свеча пробивает МА вниз и цена сейчас ниже чем МА (тренд вниз)
    elif ( ma_arr[i-1]>close_price[i-1] and ma_arr[i-1]<open_price[i-1] and close_price[i]<ma_arr[i]):
        if contract != 0 and action == 'Sell':
            #print('open price = ', open_price[i], ' close_price =', close_price[i])
            #print('Sell')
            usdt = usdt + contract*close_price[i]
            usdt_arr.append(usdt)
            contract = 0
            #print('Contract = ', contract)
            #print('Usdt = ', usdt)
        
        if volume[i-1] >  volume_prc*va_arr[i-1]:
            #print('open price = ', open_price[i], ' close_price =', close_price[i])
            
            if contract == 0 :  
                #print('Sell')
                contract = -usdt*usdt_prc/close_price[i]
                usdt = usdt + usdt*usdt_prc
                btc_old_price = close_price[i]
                #print('Contract = ', contract)
                #print('Usdt = ', usdt)
                action = 'Buy'
                #print('I want to buy')
            elif action == 'Sell' :
                #print('Sell')
                usdt = usdt + contract*close_price[i]
                usdt_arr.append(usdt)
                contract = 0
                #print('Contract = ', contract)
                #print('Usdt = ', usdt)
            else :
                pass
                #print('HODL')

print(usdt)
print(len(usdt_arr))                
plt.plot(usdt_arr)
plt.savefig("plot.png")
plt.close()
perc_arr = [usdt_arr[i]/usdt_arr[i-1] for i in range(1,len(usdt_arr))]   # на сколько процентов каждый раз увеличивается кошелек

plt.plot(perc_arr)
plt.savefig("perc.png")





