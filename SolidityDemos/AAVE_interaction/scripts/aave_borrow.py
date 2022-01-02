from scripts.utils import get_account
from brownie import config, network, interface
from scripts.convert_eth_to_weth import convert_to_weth
from web3 import Web3

amount_to_deposit = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_token_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        # generate some weth
        convert_to_weth()

    lending_pool_contract = get_lending_pool()

    # In order to send ERC20 token we need to approve it
    approve_erc20(
        amount_to_deposit, lending_pool_contract.address, erc20_token_address, account
    )

    tx = lending_pool_contract.deposit(
        erc20_token_address, amount_to_deposit, account.address, 0, {"from": account}
    )
    tx.wait(1)

    borrowable_eth, total_debt = get_borrowable_data(lending_pool_contract, account)


def get_borrowable_data(lending_pool, account):
    # get 6 parameters with tuple syntax
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        _,
        _,
        _,
    ) = lending_pool.getUserAccountData(account.address)
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")

    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender_address, erc20_address, account_address):
    # ABI - IErc20
    # Address - erc20_address
    print("Approving ERC20 token...")

    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender_address, amount, {"from": account_address})
    tx.wait(1)
    return tx


def get_lending_pool():
    # We need 1. ABI 2. Address for lending_pool_addresses_provider

    # Here we provider the "real" contract address for the interface
    # ILendingPoolAddressesProvider - ABI
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )

    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    # - Now (once again!) We need
    #   1. ABI (ILendingPool)
    #   2. Address for lending pool (lending_pool_address)
    # - Interface is compiled down into ABI
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
