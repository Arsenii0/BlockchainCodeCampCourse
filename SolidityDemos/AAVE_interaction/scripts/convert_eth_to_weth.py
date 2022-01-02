from scripts.utils import get_account
from brownie import interface, config, network


def main():
    convert_to_weth()


def convert_to_weth():
    account = get_account()

    # ArsenP : it is an interface for the contract which is already deployed on the network (eg. KOVAN)
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10 ** 18})  # deposit 0.1 ETH
    tx.wait(4)  # wait 4 blocks confirmations
    return tx
