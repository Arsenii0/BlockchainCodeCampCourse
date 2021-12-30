from brownie import accounts, config, SimpleStorage, network
from brownie.network import account

from scripts.utils import get_account


def deploy_simple_storage():
    account = get_account()
    # account = accounts.load("metamask_accout_test") # get from locally added account
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["private_key"])

    # get bytecode and abi -> create nonce -> create the contract -> create the transaction -> sigh the transaction -> send the transaction
    simple_storage_contract = SimpleStorage.deploy({"from": account})

    # do not need to add {"from": account} because it is a "view" method
    print(simple_storage_contract.getMyNumber())

    # here we do a transaction, so we need to add {"from": account}
    transaction = simple_storage_contract.storeMyNumber(15, {"from": account})
    transaction.wait(1)  # how many blocks we want to wait
    print(simple_storage_contract.getMyNumber())


def read_simple_storage_contract():
    simple_storage_contract = SimpleStorage[-1]  # -1 get the most recent deployment
    print(simple_storage_contract.getMyNumber())


def main():
    deploy_simple_storage()
    # read_simple_storage_contract()


# brownie works with local ganache-cli by default
