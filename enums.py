from enum import Enum


class DateEnum(Enum):
    TIMESTAMP = "timestamp"
    DATE = "date"
    DATE_READABLE = "date_readable"


class TypeEnum(Enum):
    TRANSACTION = "transaction"
    TYPE = "type"


class AmountEnum(Enum):
    AMOUNT = "amount"
    AMOUNTS = "amounts"


class BankEnum(Enum):
    BANK1 = "bank1"
    BANK2 = "bank2"
    BANK3 = "bank3"