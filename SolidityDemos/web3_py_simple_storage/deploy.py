from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv
import inspect

load_dotenv()


def signAndSendTransaction(transaction, private_key, abi):

    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send signed transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    return transaction_receipt


def createAndDeployContract(bytecode, abi, w3, address, private_key, nonce, chain_id):
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

    # To change the state of blockchain - only with transaction
    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": address,
            "nonce": nonce,
        }
    )

    transaction_receipt = signAndSendTransaction(transaction, private_key, abi)

    # Working with the contract, we always need:
    # Contract Address
    # Contract ABI

    # How we can interact with the contract?:
    # 1. Call -> Do not change state of the blockchain ("view" or "pure")
    # 2. Transact -> DO change state of the blockchain.

    # ArsenP : how to check method's signature
    # inspect.signaturegetargspec(w3.eth.contract)

    simple_storage_contract = w3.eth.contract(
        address=transaction_receipt.contractAddress, abi=abi
    )
    return simple_storage_contract


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        # No need to fully understand it for now
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Now we need to deploy our code (currently into virtual machine).
# Ganache is simulated (or face blockchain). It is not connected to the real blockchain

# For connecting to ganache or rinkeby

# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545")) ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/a2420dc33e5c472e8706c4271f21fe44")
)  # rinkeby


# chain_id = 1337 chain id for local ganache-cli
chain_id = 4  # chain id for Ethereum Tesnet Rinkeby
my_address = "0x74D1A0f5971486e8A538d145A01FE31476CCf710"  # 0x indicates for hexadecimal (base 16 or hex)
private_key = os.getenv("PRIVATE_KEY")
# Get the latest transaction. Used to sing up a transaction. It is a number of transaction
nonce = w3.eth.getTransactionCount(
    my_address
)  # zero because we currently do not have any transactions

print("Deploying contract...")
initial_contract = createAndDeployContract(
    bytecode, abi, w3, my_address, private_key, nonce, chain_id
)
print("Deployed!")

# Create the contract in python

print(initial_contract.functions.getMyNumber().call())

# It is just a call and do not change the transaction
# print(initial_contract.functions.storeMyNumber(15).call())

# Here we actually send storeMyNumber transaction
store_my_number_transaction = initial_contract.functions.storeMyNumber(
    15
).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        # because we already used nonce (nonce is used once for each transaction)
        "nonce": nonce + 1,
    }
)

print("Updating contract...")
tx_receipt = signAndSendTransaction(store_my_number_transaction, private_key, abi)
print("Updated!")

print(initial_contract.functions.getMyNumber().call())
