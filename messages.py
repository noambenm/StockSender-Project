def buy_now_message(current_value, average_open, usd_value, commission):
    return f"""ALERT! VOO is trading at {current_value}$, which is more than 15% below the average open price over the past month.

    Average open price: {average_open}$
    Current price: {current_value}$

    The price of USD is currently {usd_value}₪, and a VOO ETF will cost you {round(current_value * usd_value, 2)}₪.
    Your IBI buying commission is 7.5$, so the commission will be {commission}₪.

    This is a significant drop. Consider buying more VOO according to your investment strategy.
    """


def buy_opportunity_message(current_value, average_open, usd_value, commission):
    return f"""VOO is trading at {current_value}$, which is slightly lower than the average open price over the past month.

    Average open price: {average_open}$
    Current price: {current_value}$

    The price of USD is currently {usd_value}₪, and a VOO ETF will cost you {round(current_value * usd_value, 2)}₪.
    Your IBI buying commission is 7.5$, so the commission will be {commission}₪.

    This might be a good time to buy more VOO. Check your investment strategy.
    """


def normal_status_message(current_value, average_open, usd_value, commission):
    return f"""VOO is trading at {current_value}$, which is within the normal range.

    Average open price over the past month: {average_open}$
    The price of USD is currently {usd_value}₪, and a VOO ETF will cost you {round(current_value * usd_value, 2)}₪.
    Your IBI buying commission is 7.5$, so the commission will be {commission}₪.

    No significant price drop detected. No action required.
    """