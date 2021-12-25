from brownie import network, config, MockV3Aggregator
from brownie.network import accounts

DECIMALS = 18
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN:
        return accounts[0]  # get from ganache-cli
    else:
        return accounts.add(config["wallets"]["private_key"])


def deploy_mock():
    account = get_account()

    print(f"The active network is {network.show_active()} Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:  # if not yed deployed...
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
