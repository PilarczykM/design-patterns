# Strategy Pattern

The Strategy Pattern is a behavioral design pattern that allows a client to choose from a family of interchangeable algorithms at runtime. It encapsulates each algorithm and makes them interchangeable, enabling the client to vary the algorithm independently of the context that uses it.

## When to Use
- Use the Strategy Pattern when you want to define a class that will have one behavior that is similar to other behaviors in a list.
- When you need to use one of several behaviors dynamically.
- When you need to isolate the business logic of a class from the implementation details of algorithms.

# Overview

This code demonstrates the implementation focusing on a trading strategy example where different strategies are interchangeable to decide whether to buy or sell assets.

In this example, we have defined a `TradingStrategy` protocol (interface) with methods `should_buy()` and `should_sell()`, which are implemented by various concrete strategy classes.

- **`TradingStrategy`**: This protocol defines the methods that any trading strategy class should implement, allowing for interchangeable strategies.

- **`AverageTradingStrategy`**: This concrete strategy class implements a trading strategy based on price averages.

- **`MinMaxTradingStrategy`**: This concrete strategy class implements a trading strategy based on price minima and maxima.
