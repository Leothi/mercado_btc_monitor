def make_current_price_message(last_price: str, sell_price: str, buy_price: str) -> str:
    """Cria mensagem de preço atual para Telegram.

    :param last_price: Último preço.
    :type last_price: str
    :param sell_price: Preço de venda.
    :type sell_price: str
    :param buy_price: Preço de compra.
    :type buy_price: str
    :return: Mensagem final.
    :rtype: str
    """
    last_price = round(float(last_price), 1)
    sell_price = round(float(sell_price), 1)
    buy_price = round(float(buy_price), 1)

    last = f"*Último*: {last_price :>15}"
    sell = f"*Venda*: {sell_price :>16}"
    buy = f"*Compra*: {buy_price :>13}"

    last = f"*Último*: {last_price :>12}"
    sell = f"*Venda*: {sell_price :>13}"
    buy = f"*Compra*: {buy_price :>10}"

    message = '\n'.join([last, sell, buy])
    return message


def make_if_target_price_message(last_price: float, target_price: float) -> str:
    """Cria mensagem de preço alvo para Telegram.

    :param last_price: Último preço.
    :type last_price: float
    :param target_price: Preço alvo.
    :type target_price: float
    :return: Mensagem final.
    :rtype: str
    """
    last_price = round(float(last_price), 2)
    target_price = round(float(target_price), 2)

    target = f"Target: {target_price}"
    last = f"Atual: {last_price}"

    result = "Preço MENOR que target."
    if last_price >= target_price:
        result = "Preço MAIOR que target."

    message = '\n'.join([target, last, result])
    return message
