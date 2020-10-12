import numpy as np

def get_ma_va(close_price, volume, ma, volume_avarage):
    start = 0   # стартер, если среднее значение цены за 20 часов а обьема за 25, то нет смысла учитывать первые 24 часа потому что не будет данных по обьему
    if ma > volume_avarage : 
        start = ma
    else :
        start = volume_avarage
    ma_arr = []
    va_arr = []

    for i in range(start, len(close_price)): # просто arrays со средними значениями
        ma_arr.append(np.mean(close_price[i-ma:i]))
        va_arr.append(np.mean(volume[i-ma:i]))

    return start, ma_arr, va_arr
        

