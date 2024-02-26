from dataclasses import dataclass
import statistics
from typing import Callable
from exchange import Exchange

TradingStrategyFunction = Callable[[list[int]], bool]


def should_buy_avg_closure(window_size: int) -> TradingStrategyFunction:
    def should_buy_avg(prices: list[int]) -> bool:
        list_window = prices[-window_size:]
        return prices[-1] < statistics.mean(list_window)

    return should_buy_avg


def should_sell_avg_closure(window_size: int) -> TradingStrategyFunction:
    def should_sell_avg(prices: list[int]) -> bool:
        list_window = prices[-window_size:]
        return prices[-1] > statistics.mean(list_window)

    return should_sell_avg


def should_buy_min_max_closure(max_price: int) -> TradingStrategyFunction:
    def should_buy_min_max(prices: list[int]) -> bool:
        return prices[-1] < max_price

    return should_buy_min_max


def should_sell_min_max_closure(min_price: int) -> TradingStrategyFunction:
    def should_sell_min_max(prices: list[int]) -> bool:
        return prices[-1] > min_price

    return should_sell_min_max


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
    bot = TradingBot(
        exchange,
        should_buy_min_max_closure(32_000),
        should_sell_min_max_closure(32_000),
    )
    bot.run("ETH/USD")


if __name__ == "__main__":
    main()
