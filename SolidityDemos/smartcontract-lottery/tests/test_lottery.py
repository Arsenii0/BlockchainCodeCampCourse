from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery_contract = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )

    # print("Arsen debug")
    # print(lottery_contract.getEntranceFee())
    # print(Web3.toWei(0.018, "ether"))
    assert lottery_contract.getEntranceFee() > Web3.toWei(0.012, "ether")
    assert lottery_contract.getEntranceFee() < Web3.toWei(0.014, "ether")
