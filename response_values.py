from enums import (
    DateEnum,
    TypeEnum,
    AmountEnum,
)


timestamp = {
            DateEnum.DATE.value: DateEnum.TIMESTAMP.value,
            DateEnum.DATE_READABLE.value: DateEnum.TIMESTAMP.value,
        }
type = {
    TypeEnum.TRANSACTION.value: TypeEnum.TYPE.value,
}
amount = {
    AmountEnum.AMOUNTS.value: AmountEnum.AMOUNT.value,
}

RESPONSE_COLUMNS_RENAME_MAP = {**timestamp, **type, **amount}
RESPONSE_COLUMNS = ["timestamp", "type", "amount", "to", "from"]