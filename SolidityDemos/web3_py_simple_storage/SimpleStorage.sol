// JavaScript VM - test environment
// Solidity is constantly updating

// SPDX-License-Identifier: MIT - the most open license

// EVM - Ethereum Virtual Machine. So you
// can deploy your smart contracts even for others
// (non-ethereum blockchains). All code is compiled to EVM

pragma solidity ^0.6.0;

contract SimpleStorage {
    address my_address = 0x74D1A0f5971486e8A538d145A01FE31476CCf710; // some time of ethereum address

    // default initialization
    uint256 public my_number;

    // every time we deploy a contract or make
    // a transaction - it will cost some gas
    // calling (non-const) function is a transaction

    // dynamic array
    string[] public string_dynamic_array;

    function storeMyNumber(uint256 _my_number) public {
        my_number = _my_number;
    }

    // view, pure. Do not change state of blockchain
    // view - const (c++), have some state
    // pure - is like view but DO NOT return any state of blockchain. So it is more strict
    function getMyNumber() public view returns (uint256) {
        return my_number;
    }

    // memory - data will be only stored during the execution of the function. It will be destroyed afterwards
    // storage - data persists even after function executes. Keep variable forever
    function addString(string memory _str) public {
        string_dynamic_array.push(_str);
    }
}
