from dataclasses import dataclass
from enum import Enum


class Code(str, Enum):
    """Currency codes"""

    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    JPY = 'JPY'

    # TODO: Add more Currencies


@dataclass
class Currency:
    """
    Currency (ISO 4217).
    code: The currency code.
    name: The currency name.
    num: The currency number.
    symbol: The currency symbol.
    decimal: The number of decimal places for the currency.
    countries: The list of countries where the currency is used.
    """

    code: Code
    name: str
    num: int
    symbol: str
    decimal: int
    countries: list[str]


currencies: dict[Code, Currency] = {
    Code.USD: Currency(Code.USD, 'US Dollar', 840, '$', 2, ['United States']),
    Code.EUR: Currency(Code.EUR, 'Euro', 978, '€', 2, ['European Union']),
    Code.GBP: Currency(Code.GBP, 'British Pound', 826, '£', 2, ['United Kingdom']),
    Code.JPY: Currency(Code.JPY, 'Japanese Yen', 392, '¥', 0, ['Japan']),
    Code.RUB: Currency(Code.RUB, 'Russian Ruble', 643, '₽', 2, ['Russia']),
}
