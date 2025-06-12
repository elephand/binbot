import time
import logging
from config import bot, pairs, log
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

def main():
    sync_time(bot, log, pause=False)
    conn = sqlite3.connect('orders.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    make_initial_tables(cursor)

    sync_time(bot, log, pause=False)

    open_orders = get_db_open_orders(cursor)
    running_pairs = get_db_running_pairs(cursor)

    for pair in pairs:
        if not pair['active']:
            continue

        symbol = pair['quote'] + pair['base']
        if symbol in running_pairs:
            continue

        price_info = bot.futures_symbol_ticker(symbol=symbol)
        current_price = float(price_info['price'])

        quantity = adjust_to_step(pair['spend_sum'] / current_price, bot.get_symbol_info(symbol)['quantity_step'])

        order = bot.futures_create_order(
        symbol=symbol,
            side='BUY',
            type='MARKET',
            quantity=quantity
        )

        log.debug(f"Ответ от Binance на создание ордера: {order}")

        if 'orderId' not in order:
            log.error(f"Ошибка при создании ордера: {order}")
            return

        add_db_new_order(cursor, conn, symbol, order['orderId'], quantity, current_price)

        log.info(f"Открыт ордер BUY {symbol} по цене {current_price}")

    time.sleep(60)

if __name__ == "__main__":
    main()