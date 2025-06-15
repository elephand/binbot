import logging
import os

from binance_api import BinanceFutures

bot = BinanceFutures(
    API_KEY='1YsAEkVPj8iAV2NVJno6fckJ6UnrlEuK3UiDrgyZv28WsEMSNqd3DqUMVJo8aZmR',
    API_SECRET='rBPVmffl1ZpXpFKwJUdnFruOLano1uGx45bRlphAZORPJWVvMdjw4mxQtDVqOPLL'
)

"""
    Пропишите пары, на которые будет идти торговля.
    base - это базовая пара (например USDT) — в фьючерсах это всегда вторая часть контракта.
    quote - это актив, которым торгуем (например BTC, ETH и т.п.)
"""
pairs = [
   {
        'base': 'USDT',
        'quote': 'ETH',
        'spend_sum': 50,  # Сколько USDT тратить на вход в позицию
        'profit_markup': 1, # Какой навар нужен с каждой сделки? (1=1%)
        'use_stop_loss': False, # Нужно ли закрывать с убытком при падении цены
        'stop_loss': 1.5, # На сколько должна упасть цена, чтобы закрыть с убытком
        'active': True,
        
        # Параметры SuperTrend для данной пары:
        'supertrend': {
            'source': 'hl2',
            'atr_period': 10,
            'multiplier': 3.0,
            'change_atr_calculate': False
        }
    },
    {
        'base': 'USDT',
        'quote': 'NEO',
        'spend_sum': 10,
        'profit_markup': 1,
        'use_stop_loss': False,
        'stop_loss': 2,
        'active': False,
        
        # Параметры SuperTrend для данной пары:
        'supertrend': {
            'source': 'hl2',
            'atr_period': 10,
            'multiplier': 3.0,
            'change_atr_calculate': False
        }
    }
]

KLINES_LIMITS = 200
POINTS_TO_ENTER = 7

USE_OPEN_CANDLES = True

TIMEFRAME = "1m"
'''
    Допустимые интервалы:
    •    1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
'''

#Подключаем логирование
logging.basicConfig(
    format="%(asctime)s [%(levelname)-5.5s] %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("{path}/logs/{fname}.log".format(
            path=os.path.dirname(os.path.abspath(__file__)),
            fname="binance_futures")),
        logging.StreamHandler()
    ])
log = logging.getLogger('')



'''
import logging
import os

from binance_api import Binance

bot = Binance(
    API_KEY='7C7AwvoJcteqIHVZY3fBJ0ml3eYuhgObNFAQny9CvTG7muntbAwL4QH8Qkrh3qCl',
    API_SECRET='jDi6JSNJFHFawd3KxLJkSJmr8olbItcTzQyrLcQfAQzpL1KFhSuv0CjV2SPEiqbM'
)

"""
    Пропишите пары, на которые будет идти торговля.
    base - это базовая пара (BTC, ETH,  BNB, USDT) - то, что на бинансе пишется в табличке сверху
    quote - это квотируемая валюта. Например, для торгов по паре NEO/USDT базовая валюта USDT, NEO - квотируемая
"""
pairs = [
   {
        'base': 'ETH',
        'quote': 'ADA',
        'spend_sum': 0.02,  # Сколько тратить base каждый раз при покупке quote
        'profit_markup': 1, # Какой навар нужен с каждой сделки? (1=1%)
        'use_stop_loss': False, # Нужно ли продавать с убытком при падении цены
        'stop_loss': 1, # 1% - На сколько должна упасть цена, что бы продавать с убытком
        'active': True,
    }, {
        'base': 'USDT',
        'quote': 'NEO',
        'spend_sum': 11,  # Сколько тратить base каждый раз при покупке quote
        'profit_markup': 1, # Какой навар нужен с каждой сделки? (0.001 = 0.1%)
        'use_stop_loss': False, # Нужно ли продавать с убытком при падении цены
        'stop_loss': 2, # 2%  - На сколько должна упасть цена, что бы продавать с убытком
        'active': False,
    }
]

KLINES_LIMITS = 200
POINTS_TO_ENTER = 7


"""
    USE_OPEN_CANDLES = True - использовать последнюю (текущую) свечу для расчетов
    USE_OPEN_CANDLES = False - Использовать только закрытые свечи

    Например, если USE_OPEN_CANDLES = False и таймфрейм часовой, и время 13:21, то будут браться свечи до 13:00.
    После 14:00 свеча с 13:00 по 14:00 тоже попадет в выборку, но не будет браться 14:00 - 15:00 и т.п.
"""
USE_OPEN_CANDLES = True 

TIMEFRAME = "1h"

    Допустимые интервалы:
    •    1m     // 1 минута
    •    3m     // 3 минуты
    •    5m    // 5 минут
    •    15m  // 15 минут
    •    30m    // 30 минут
    •    1h    // 1 час
    •    2h    // 2 часа
    •    4h    // 4 часа
    •    6h    // 6 часов
    •    8h    // 8 часов
    •    12h    // 12 часов
    •    1d    // 1 день
    •    3d    // 3 дня
    •    1w    // 1 неделя
    •    1M    // 1 месяц





# Подключаем логирование
logging.basicConfig(
    format="%(asctime)s [%(levelname)-5.5s] %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("{path}/logs/{fname}.log".format(path=os.path.dirname(os.path.abspath(__file__)), fname="binance")),
        logging.StreamHandler()
    ])
log = logging.getLogger('')

'''