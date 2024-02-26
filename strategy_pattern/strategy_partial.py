from dataclasses import dataclass
from functools import partial
import statistics
from typing import Callable
from exchange import Exchange

TradingStrategyFunction = Callable[[list[int]], bool]


def should_buy_avg(prices: list[int], window_size: int) -> bool:
    list_window = prices[-window_size:]
    return prices[-1] < statistics.mean(list_window)


def should_sell_avg(prices: list[int], window_size: int) -> bool:
    list_window = prices[-window_size:]
    return prices[-1] > statistics.mean(list_window)


def should_buy_min_max(prices: list[int], max_price: int) -> bool:
    return prices[-1] < max_price


def should_sell_min_max(prices: list[int], min_price: int) -> bool:
    return prices[-1] > min_price


@dataclass
class TradingBot:
    exchange: Exchange
    buy_strategy: TradingStrategyFunction
    sell_strategy: TradingStrategyFunction

    def run(self, symbol: str) -> None:
        prices = self.exchange.get_market_data(symbol)
        if self.buy_strategy(prices):
            self.exchange.buy(symbol, 10)
        elif self.sell_strategy(prices):
            self.exchange.sell(symbol, 10)
        else:
            print(f"No action needed for {symbol}.")


def main() -> None:
    exchange = Exchange()

    # create the trading bot and run the bot once
    buy_strategy = partial(should_buy_avg, window_size=10)
    sell_strategy = partial(should_sell_avg, window_size=10)
    bot = TradingBot(exchange, buy_strategy, sell_strategy)
    bot.run("ETH/USD")


if __name__ == "__main__":
    main()
