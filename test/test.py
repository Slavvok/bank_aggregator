import pytest
import pandas as pd
from pytest_mock import MockFixture
from main import Orchestrator
from exceptions import NoBankException


BANK1_DF = pd.DataFrame.from_dict(
    {'timestamp': {0: 'Oct 1 2019', 1: 'Oct 2 2019'},
     'type': {0: 'remove', 1: 'add'}, 'amount': {0: 99.1, 1: 2000.1},
     'to': {0: 182, 1: 198}, 'from': {0: 198, 1: 188}}
)
BANK1_DF_BAD = pd.DataFrame.from_dict(
    {'time': {0: 'Oct 1 2019', 1: 'Oct 2 2019'},
     'to': {0: 182, 1: 198}, 'from': {0: 198, 1: 188}}
)
BANK2_DF = pd.DataFrame.from_dict(
    {'date': {0: '03-10-2019', 1: '04-10-2019'}, 'transaction': {0: 'remove', 1: 'add'},
     'amounts': {0: 99.99, 1: 2123.99}, 'to': {0: 182, 1: 198}, 'from': {0: 198, 1: 188}}
)
BANK3_DF = pd.DataFrame.from_dict(
    {'date_readable': {0: '5 Oct 2019', 1: '6 Oct 2019'}, 'type': {0: 'remove', 1: 'add'},
     'euro': {0: 5, 1: 1060}, 'cents': {0: 44, 1: 44}, 'to': {0: 182, 1: 198}, 'from': {0: 198, 1: 188}}
)

RESULT_DF = pd.DataFrame(
    {'timestamp': {0: '01-10-2019', 1: '02-10-2019', 2: '03-10-2019', 3: '04-10-2019', 4: '05-10-2019', 5: '06-10-2019'},
     'type': {0: 'remove', 1: 'add', 2: 'remove', 3: 'add', 4: 'remove', 5: 'add'},
     'amount': {0: 99.1, 1: 2000.1, 2: 99.99, 3: 2123.99, 4: 5.44, 5: 1060.44},
     'to': {0: 182, 1: 198, 2: 182, 3: 198, 4: 182, 5: 198}, 'from': {0: 198, 1: 188, 2: 198, 3: 188, 4: 198, 5: 188}}
)


@pytest.fixture(autouse=True)
def mock_base_bank(mocker: MockFixture):
    mocker.patch("banks.BankBase.transfer_data")
    # mocker.patch("banks.BankBase.validate")


def test_main_success(mocker: MockFixture):
    # GIVEN
    mocker.patch("banks.Bank1.transfer_data")
    mocker.patch("banks.Bank2.transfer_data")
    mocker.patch("banks.Bank3.transfer_data")

    mocker.patch("pandas.read_csv", return_value=BANK1_DF)
    mocker.patch("pandas.read_csv", return_value=BANK2_DF)
    mocker.patch("pandas.read_csv", return_value=BANK3_DF)

    mocker.patch("pandas.concat", return_value=RESULT_DF)
    mock_csv = mocker.patch("main.Orchestrator.to_csv")

    # WHEN
    o = Orchestrator()
    o.process()

    # THEN
    mock_csv.assert_called()


def test_no_bank_exception(mocker: MockFixture):
    # GIVEN
    mocker.patch("pandas.read_csv", return_value=BANK1_DF)
    mocker.patch("pandas.read_csv", return_value=BANK3_DF)
    mock_fetch_bank = mocker.patch("main.Orchestrator.fetch_bank")
    mock_fetch_bank.side_effect = NoBankException()

    # WHEN
    o = Orchestrator()
    with pytest.raises(NoBankException):
        o.process()

    # THEN

    mock_fetch_bank.assert_called()


def test_file_not_found_error(mocker: MockFixture):
    # GIVEN
    mocker.patch("pandas.read_csv", return_value=BANK1_DF)
    bank2 = mocker.patch("pandas.read_csv")
    bank2.side_effect = FileNotFoundError()
    mocker.patch("pandas.read_csv", return_value=BANK3_DF)
    mock_fetch_bank = mocker.patch("main.Orchestrator.fetch_bank")
    mock_fetch_bank.side_effect = FileNotFoundError()

    # WHEN
    o = Orchestrator()
    with pytest.raises(FileNotFoundError):
        o.process()

    # THEN

    mock_fetch_bank.assert_called()


def test_bank1_value_error(mocker: MockFixture):
    # GIVEN
    mock_bank1 = mocker.patch("banks.Bank1.transfer_data")
    mock_bank1.side_effect = ValueError()

    mocker.patch("pandas.read_csv", return_value=BANK1_DF_BAD)

    # WHEN
    o = Orchestrator()
    with pytest.raises(ValueError):
        o.process()

    # THEN
    mock_bank1.assert_called()
