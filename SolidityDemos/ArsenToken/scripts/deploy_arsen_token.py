from brownie import accounts, config, ArsenToken, network
from brownie.network import account

LOCAL_BLOCKCHAIN = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN:
        return accounts[0]  # get from ganache-cli
    else:
        return accounts.add(config["wallets"]["private_key"])


def deploy_arsen_token():
    account = get_account()

    # get bytecode and abi -> create nonce -> create the contract -> create the transaction -> sigh the transaction -> send the transaction
    arsen_token_contract = ArsenToken.deploy(100, {"from": account})


def get_arsen_token_name():
    arsen_token_contract = ArsenToken[-1]  # -1 get the most recent deployment
    return arsen_token_contract.name()


def main():
    deploy_arsen_token()
    print(get_arsen_token_name())
