def buy_now_message(most_recent_open, average_open, currency_price, commission):
    return f"""ALERT! VOO opened at {most_recent_open}$, which is more than 15% below the average open price over the past month.

    Average open price: {average_open}$
    Current price: {most_recent_open}$

    The price of USD is currently {currency_price}₪, and a VOO ETF will cost you {round(most_recent_open * currency_price, 2)}₪.
    Your IBI buying commission is 7.5$, so the commission will be {commission}₪.

    This is a significant drop. Consider buying more VOO according to your investment strategy.
    """


def buy_opportunity_message(most_recent_open, average_open, currency_price, commission):
    return f"""VOO opened at {most_recent_open}$, which is slightly lower than the average open price over the past month.

    Average open price: {average_open}$
    Current price: {most_recent_open}$

    The price of USD is currently {currency_price}₪, and a VOO ETF will cost you {round(most_recent_open * currency_price, 2)}₪.
    Your IBI buying commission is 7.5$, so the commission will be {commission}₪.

    This might be a good time to buy more VOO. Check your investment strategy.
    """


def normal_status_message(most_recent_open, average_open, currency_price, commission):
    return f"""VOO is trading at {most_recent_open}$, which is within the normal range.

    Average open price over the past month: {average_open}$
    The price of USD is currently {currency_price}₪, and a VOO ETF will cost you {round(most_recent_open * currency_price, 2)}₪.
    Your IBI buying commission is 7.5$, so the commission will be {commission}₪.

    No significant price drop detected. No action required.
    """