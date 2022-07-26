import logging
import os
import glob

import pandas as pd

from logging import getLogger

from banks import (
    Bank1,
    Bank2,
    Bank3,
)
from enums import BankEnum
from exceptions import NoBankException
from response_values import RESPONSE_COLUMNS

logging.basicConfig()
logger = getLogger(__name__)
logger.setLevel("INFO")

PROJECT_PATH = os.path.abspath(".")
BANKS_PATH = os.path.join(PROJECT_PATH, "data")
BANKS_LIST = glob.glob(os.path.join(BANKS_PATH, "bank*"))
OUTPUT_FILE = "result.csv"


class Orchestrator:
    def process(self):
        logger.info("Starting process")
        banks = [self.fetch_bank(file) for file in BANKS_LIST]
        [bank.transfer_data() for bank in banks]
        result = pd.concat([bank.df for bank in banks], ignore_index=True)
        result = result[RESPONSE_COLUMNS]
        self.to_csv(result)

    def fetch_bank(self, file):
        try:
            data = pd.read_csv(file)
            bank = os.path.basename(file).replace(".csv", "")
            # Could be done for folder name afterwards as it's more lifelike scenario than filename
            if bank == BankEnum.BANK1.value:
                return Bank1(data)
            elif bank == BankEnum.BANK2.value:
                return Bank2(data)
            elif bank == BankEnum.BANK3.value:
                return Bank3(data)
        except FileNotFoundError as e:
            message = f"File {file} has not been found. Exception e"
            logger.error(message)
            raise e
        else:
            message = f"There is no such bank: {bank}"
            logger.error(message)
            raise NoBankException(message)

    def to_csv(self, banks: pd.DataFrame):
        banks.to_csv(os.path.join(BANKS_PATH, OUTPUT_FILE), index=False)
        logger.info(f"File {OUTPUT_FILE} has been successfully saved to {BANKS_PATH}")


if __name__ == '__main__':
    b = Orchestrator()
    b.process()
