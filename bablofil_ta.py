# bablofil_ta.py
# Вспомогательные технические алгоритмы

import math

def true_range(high_vals, low_vals, close_vals):
    """True range для серии баров."""
    tr_vals = [high_vals[0] - low_vals[0]]
    for i in range(1, len(high_vals)):
        tr_vals.append(max(high_vals[i] - low_vals[i],
                            abs(high_vals[i] - close_vals[i-1]),
                            abs(low_vals[i] - close_vals[i-1])))
    return tr_vals

def average_true_range(high_vals, low_vals, close_vals, period):
    """Average true range (для SuperTrend). Используем простой метод."""
    tr_vals = true_range(high_vals, low_vals, close_vals)
    atr_vals = [sum(tr_vals[:period]) / period]
    for i in range(period, len(tr_vals)):
        atr_vals.append((atr_vals[-1] * (period - 1) + tr_vals[i]) / period)
    return atr_vals

def calculate_super_trend(src_vals, high_vals, low_vals, period, multiplier, change_atr=False):
    """
    Расчет SuperTrend. 
    src_vals - среднее значение бара (например, hl2).
    high_vals, low_vals - серии high и low.
    period - период ATR.
    multiplier - множитель.
    change_atr - метод изменения ATR (не используется здесь, но может быть внедрен).
    """

    atr_vals = average_true_range(high_vals, low_vals, src_vals, period)

    upper_band = [s + multiplier * a for s, a in zip(src_vals, atr_vals)]

    lower_band = [s - multiplier * a for s, a in zip(src_vals, atr_vals)]

    super_trend = [0] * len(src_vals)

    direction = 1  # направление тренда; 1 - восходящая, -1 - нисходящая

    for i in range(1, len(src_vals)):
        if direction == 1:
            if low_vals[i] < upper_band[i-1]:
                direction = -1
        else:
            if high_vals[i] > lower_band[i-1]:
                direction = 1

        if direction == 1:
            lower_band[i] = max(lower_band[i], lower_band[i-1])
            super_trend[i] = lower_band[i]
        else:
            upper_band[i] = min(upper_band[i], upper_band[i-1])
            super_trend[i] = upper_band[i]

    return super_trend