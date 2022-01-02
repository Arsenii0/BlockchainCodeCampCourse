1. Convert ETH to WETH
2. Deposit some WETH to AAVE
3. Borrow some asset with the deposited ETH
    - Try to sell the borrowed asset.
4. Repay everything back 

Here we won't deploy our own contracts. We will interact with the existing
contracts on the Kovan network:
Integration test: Kovan
Unit tests: Mainnet-for (because we do not use Oracle)
[We should use a Default testing network while working with Oracles]