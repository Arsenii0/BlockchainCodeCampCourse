from brownie import FundMe, MockV3Aggregator, network, config
from scripts.utils import get_account, deploy_mock, LOCAL_BLOCKCHAIN


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mock()
        # -1 means use the most recent deployed contract
        price_feed_address = MockV3Aggregator[-1].address

    fund_me_contract = FundMe.deploy(price_feed_address, {"from": account})
    return fund_me_contract


def main():
    deploy_fund_me()
