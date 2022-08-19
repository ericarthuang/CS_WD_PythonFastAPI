import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount(0)

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize(
    "x, y, z",
    [
        (5, 3, 8),
        (1, 2, 3),
        (4, 8, 12)
    ]
)
def test_add(x, y, z):
    print("testing add func")
    assert add(x, y) == z


def test_subtract():
    assert subtract(3,1) == 2


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_initail_account(bank_account):
    assert bank_account.balance == 50


@pytest.mark.parametrize(
    "deposited, withdrew, balanced",
    [
        (200, 100, 100),
        (7, 1, 6),
        (12, 4, 8),
    ]
)
def test_bank_transaction(zero_bank_account, deposited, withdrew, balanced):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == balanced


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
