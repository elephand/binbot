class BaseTrade(object):
    def _init_(self, trade_id, trade_rate, trade_amount, trade_type,
                 trade_total=None, trade_fee=None, fee_type=None,
                 position_side=None, margin_type=None, leverage=None,
                 **kwargs):

        self.trade_id = trade_id
        self.trade_rate = trade_rate
        self.trade_amount = trade_amount
        self.trade_type = trade_type  # 'buy' or 'sell'
        self.trade_fee = trade_fee
        self.fee_type = fee_type

        self.position_side = position_side  # 'LONG' or 'SHORT' (if applicable)
        self.margin_type = margin_type  # 'isolated' or 'cross' (if provided)
        self.leverage = leverage  # optional, numeric

        if not trade_total:
            self.trade_total = trade_rate * trade_amount
        else:
            self.trade_total = trade_total

        # Устанавливаем прочие свойства для представления класса
        for key, value in kwargs.items():
            setattr(self, key, value)