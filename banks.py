import logging
import pandas as pd
from abc import ABC
from request_values import Bank1Model, Bank2Model, Bank3Model

from response_values import RESPONSE_COLUMNS_RENAME_MAP
RESPONSE_DATETIME_FORMAT = "%d-%m-%Y"

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class BankBase(ABC):
    DATE_FORMAT = None
    VALIDATOR = None

    def __init__(self, df):
        self.df = df

    def transfer_data(self):
        self.validate()
        self.df = self.df.rename(columns=RESPONSE_COLUMNS_RENAME_MAP)
        self.transfer_time()

    def transfer_time(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], format=self.DATE_FORMAT)
        self.df['timestamp'] = self.df['timestamp'].dt.strftime(RESPONSE_DATETIME_FORMAT)

    def validate(self):
        """
        Validation should be far more advanced though
        """
        try:
            self.VALIDATOR.validate(self.df.iloc[0].to_dict())
        except ValueError as e:
            logger.error(f"Validation failed for {self.__class__}. Exception: {e}")
            raise e
        else:
            logger.info(f"Validation passsed for {self.__class__}")


class Bank1(BankBase):
    DATE_FORMAT = "%b %d %Y"
    VALIDATOR = Bank1Model

    def transfer_data(self):
        super().transfer_data()


class Bank2(BankBase):
    DATE_FORMAT = "%d-%m-%Y"
    VALIDATOR = Bank2Model

    def transfer_data(self):
        super().transfer_data()


class Bank3(BankBase):
    DATE_FORMAT = "%d %b %Y"
    VALIDATOR = Bank3Model

    def transfer_data(self):
        """
        Data we are getting should follow our expectations.
        This is why I've implemented banks classes in the first place.
        """
        self.df["amount"] = self.df.apply(lambda x: self.transf(x), axis=1)
        super().transfer_data()

    def transf(self, x):
        return float(f"{x['euro']}.{x['cents']}")