from brownie import SimpleStorage, accounts
from brownie import network, exceptions
from brownie.network import account
from scripts.utils import LOCAL_BLOCKCHAIN, get_account
from scripts.deploy_fund_me import deploy_fund_me
import pytest


def test_simple_storage_deploy():
    # Arrange
    account = accounts[0]

    # Act
    simple_storage_account = SimpleStorage.deploy({"from": account})

    # Assert
    expected_initial_number = 0
    assert simple_storage_account.getMyNumber() == expected_initial_number


def test_fund_me_and_withdraw():
    account = get_account()
    fund_me_contract = deploy_fund_me()
    tx_fund = fund_me_contract.fund({"from": account, "value": 500})
    tx_fund.wait(1)  # wait for the single block confirmation
    assert fund_me_contract.addressToAmountFunded(account.address) == 500

    tx_withdraw = fund_me_contract.withdraw({"from": account})
    tx_fund.wait(1)  # wait for the single block confirmation
    assert fund_me_contract.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    fund_me_contract = deploy_fund_me()
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me_contract.withdraw({"from": bad_actor})
