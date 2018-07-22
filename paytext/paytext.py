# pyre-strict

"""
This module helps you work with payment texts such as
"*4321 29.06 USD 50.00 ITUNES.COM/BILL Rate: 1.0000".
"""
from re import compile as compile_regex
from typing import List, Any

import iso4217parse


class PaymentText:
    """
    Use this class to represent your payment text.
    """
    parts: List[str] = []

    def __init__(self, text: str) -> None:
        self.parts = text.split()

    def __repr__(self) -> str:
        return ' '.join(self.parts)

    def generalize(self) -> None:
        """
        Remove all parts of the strings that are specific to just this payment,
        in order to have a string that is the same across different payments of
        the same type (e.g. a monthly payment to Apple for iCloud storage).

        :return:
        """
        self._clean_leading_card_number()
        self._clean_leading_date()
        self._clean_leading_amount_and_currency()
        self._clean_trailing_exchange_rate()
        self._clean_trailing_date()
        self._clean_trailing_amount_and_currency()

    def _clean_leading_card_number(self)-> None:
        pattern = compile_regex(r'\*\d{4}')

        try:
            if pattern.match(self.parts[0]):
                del self.parts[0]
        except IndexError:
            pass

    def _clean_leading_date(self)-> None:
        pattern = compile_regex(r'\d{2}\.\d{2}')

        try:
            if pattern.match(self.parts[0]):
                del self.parts[0]
        except IndexError:
            pass

    def _clean_leading_amount_and_currency(self)-> None:
        try:
            currency: Any = iso4217parse.by_alpha3(self.parts[0])
            if isinstance(currency, iso4217parse.Currency):
                del self.parts[0]
                del self.parts[0]
        except IndexError:
            pass

    def _clean_trailing_exchange_rate(self)-> None:
        pattern = compile_regex(r'\d{1}\.\d{4}')

        try:
            if pattern.match(self.parts[-1]):
                del self.parts[-1]
                del self.parts[-1]
        except IndexError:
            pass

    def _clean_trailing_date(self)-> None:
        pattern = compile_regex(r'\d{2}\.\d{2}\.\d{2}')

        try:
            if pattern.match(self.parts[-1]):
                del self.parts[-1]

                pattern = compile_regex(r'.+:')

                if pattern.match(self.parts[-1]):
                    del self.parts[-1]
        except IndexError:
            pass

    def _clean_trailing_amount_and_currency(self)-> None:
        pattern = compile_regex(r'\d+,\d{2}')

        try:
            if pattern.match(self.parts[-1]):
                del self.parts[-1]

                currency: Any = iso4217parse.by_alpha3(self.parts[-1])
                if isinstance(currency, iso4217parse.Currency):
                    del self.parts[-1]
        except IndexError:
            pass
