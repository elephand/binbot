import time
import logging
from config import bot, pairs, log, KLINES_LIMITS, USE_OPEN_CANDLES, TIMEFRAME
from db_queries import (
    make_initial_tables,
    get_db_open_orders,
    get_db_running_pairs,
    add_db_new_order,
    update_buy_rate,
    update_sell_rate,
    store_sell_order,
)
from misc import (
    adjust_to_step,
    sync_time,
    calc_buy_avg_rate,
    calc_sell_avg_rate,
    get_order_trades,
)
import sqlite3

# Импорт SuperTrend из bablofil_ta
from bablofil_ta import calculate_super_trend

def main():
    """Основной алгоритм работы с ордерами с помощью SuperTrend."""
    logging.basicConfig(filename='bot.log', level=logging.DEBUG, 
                        format=' %(asctime)s [ %(levelname)s ] %(message)s')
    logging.debug("Бот запускается.")
    bot.sync_time()  # Синхронизация времени с сервером Binance
    conn = sqlite3.connect('orders.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    make_initial_tables(cursor)

    #sync_time(bot, log, pause=False)

    open_orders = get_db_open_orders(cursor)
    running_pairs = get_db_running_pairs(cursor)

    for pair in pairs:
        if not pair['active']:
            logging.debug(f"{pair['base']}/{pair['quote']} отключена.")
            continue

        symbol = pair['quote'] + pair['base']
        
        if symbol in running_pairs:
            logging.debug(f"{symbol} уже имеет активные позиции.")
            continue
            
        # Получаем свечные данные
        logging.debug(f"Начинаем анализ {symbol}.")
        klines = bot.futures_klines(
            symbol=symbol,
            interval=TIMEFRAME,
            limit=KLINES_LIMITS
        )
        
        if USE_OPEN_CANDLES:
            df = klines
        else:
            df = klines[:-1]

        close_vals = [float(k[4]) for k in df]
        high_vals = [float(k[2]) for k in df]
        low_vals = [float(k[3]) for k in df]

        src = pair['supertrend']['source']

        if src == 'hl2':
            src_vals = [(h + l) / 2 for h, l in zip(high_vals, low_vals)]

        elif src == 'close':
            src_vals = close_vals

        else:
            src_vals = close_vals

        period = pair['supertrend']['atr_period']
        multiplier = pair['supertrend']['multiplier']

        change_atr = pair['supertrend']['change_atr_calculate']
        
        logging.debug(f"Начинаем расчет SuperTrend для {symbol}")
        try:
            direction = calculate_super_trend(
                src_vals, high_vals, low_vals,
                period, multiplier, change_atr
            )
        except Exception as e:   
            logging.error(f"Не получилось рассчитать SuperTrend для {symbol}: {e}")
            continue
        
        if not direction:
            logging.error(f"Не получили направление SuperTrend для {symbol}")
            continue

        #if direction[-1] > 0:
        last_trend = direction[-1] # Восходящая точка SuperTrend - можем искать точку на LONG  
        logging.debug(f"SuperTrend last_trend {symbol}: {last_trend}")
            

        price_info = bot.futures_symbol_ticker(symbol=symbol)
        current_price = float(price_info['price'])
        
        logging.debug(f"{symbol} current price: {current_price}")

        qty = adjust_to_step(pair['spend_sum'] / current_price, bot.get_symbol_info(symbol)['quantity_step'])
        if last_trend > 0:
            side = 'BUY'
            direction_txt = "LONG"
        else:
            side = 'SELL'
            direction_txt = "SHORT"

        logging.debug(f"Отправляем MARKET {side} {symbol} qty:{qty}")
            
            # Восходящая точка SuperTrend - LONG

        order = bot.futures_create_order(
            symbol=symbol,
            side=side,
            method='POST',
            type='MARKET',
            quantity=qty
        )
        logging.debug(f"Ответ от Binance на создание ордера {direction_txt}: {order}")

        if 'orderId' not in order:
            logging.error(f"Не получилось выполнить {direction_txt} {symbol}: {order}")
            continue

        add_db_new_order(cursor, conn, symbol, order['orderId'], qty, current_price)

        logging.info(f"Открыт ордер {direction_txt} {symbol} по цене {current_price}")
    
    logging.debug("Цикл завершен.")
    time.sleep(60)

if __name__ == "__main__":
    main()