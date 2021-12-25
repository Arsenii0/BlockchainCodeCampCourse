from brownie import FundMe
from scripts.utils import get_account


def fund():
    fund_me = FundMe[-1]  # get last deployed contract
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()

    # "from": account - set msg.sender
    # "value": 500 - set msg.value
    fund_me.fund({"from": account, "value": 500})


def withdraw():
    fund_me = FundMe[-1]  # get last deployed contract
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
