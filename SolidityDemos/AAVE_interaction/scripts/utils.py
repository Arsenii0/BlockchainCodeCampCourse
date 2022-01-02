from brownie import network, config
from brownie.network import accounts

LOCAL_BLOCKCHAIN = ["development", "ganache-local", "ganache"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN:
        return accounts[0]  # get from ganache-cli
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["private_key"])

    assert True
    return None
