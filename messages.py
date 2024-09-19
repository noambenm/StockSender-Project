def buy_now_message(most_recent_open, average_open, currency_price, commission):
    return (
        f"ALERT! VOO opened at {most_recent_open}$, which is more than 15% below the average open price over the past month.\n\n"
        f"Average open price: {average_open}$\n"
        f"Current price: {most_recent_open}$\n\n"
        f"The price of USD is currently {currency_price}₪, and a VOO ETF will cost you {round(most_recent_open * currency_price, 2)}₪\n"
        f"Your IBI buying commission is 7.5$, so the commission will be {commission}₪\n\n"
        "This is a significant drop. Consider buying more VOO according to your investment strategy.\n"
    )

def buy_opportunity_message(most_recent_open, average_open, currency_price, commission):
    return (
        f"VOO opened at {most_recent_open}$, which is slightly lower than the average open price over the past month.\n\n"
        f"Average open price: {average_open}$\n"
        f"Current price: {most_recent_open}$\n"
        f"The price of USD is currently {currency_price}₪, and a VOO ETF will cost you {round(most_recent_open * currency_price, 2)}₪\n"
        f"Your IBI buying commission is 7.5$, so the commission will be {commission}₪\n\n"
        "This might be a good time to buy more VOO. Check your investment strategy."
    )

def normal_status_message(most_recent_open, average_open, currency_price, commission):
    return (
        f"VOO is trading at {most_recent_open}$, which is within the normal range.\n\n"
        f"Average open price over the past month: {average_open}$\n"
        f"The price of USD is currently {currency_price}₪, and a VOO ETF will cost you {round(most_recent_open * currency_price, 2)}₪\n"
        f"Your IBI buying commission is 7.5$, so the commission will be {commission}₪\n\n"
        "No significant price drop detected. No action required."
    )