from web3 import Web3, HTTPProvider
import json
from utils import *

web3 = Web3(HTTPProvider('http://192.168.80.129:8545'))

class MyContract:

    def __init__(self, wasm_file, abi_file, **kwargs):
        with open(wasm_file, 'rb') as f:
            self.code_hex = '0x' + f.read().hex()
        with open(abi_file, 'r') as f:
            self.abi = json.load(f)
        self.raw_contract = web3.eth.contract(abi=self.abi, bytecode=self.code_hex)
        self.tx_hash = kwargs.get("tx_hash", 0x0)
        self.contract_addr = self.get_contract_addr() if self.tx_hash != 0x0 else kwargs.get("contract_addr", 0x0)

    def transact(self, func_name, account, *args):
        accounts = get_accounts()

        if func_name == "constructor":
           unsigned_contract_tx = self.raw_contract.constructor(*args).buildTransaction(
               dict(
                   nonce=web3.eth.getTransactionCount(account),
                   gasPrice=web3.eth.gasPrice,
                   gas=7000000
               )
           )
        else:
            unsigned_contract_tx = getattr(self.raw_contract.functions, func_name)(*args).buildTransaction(
                dict(
                    nonce=web3.eth.getTransactionCount(account),
                    gasPrice=web3.eth.gasPrice,
                    gas=7000000,
                    to=self.contract_addr
                )
            )
        # unsigned_contract_tx['gas'] = web3.eth.estimateGas(unsigned_contract_tx) + 10000
        signed_contract_tx = web3.eth.account.signTransaction(unsigned_contract_tx, accounts[account])
        self.tx_hash = web3.eth.sendRawTransaction(signed_contract_tx.rawTransaction)
        return self.tx_hash

    def call(self, func_name, account, *args):
        accounts = get_accounts()
        deployed_contract = web3.eth.contract(
            address=self.contract_addr,
            abi=self.abi
        )
        if account:
            result = getattr(deployed_contract.functions, func_name)(*args).call({"from": account})
        else:
            result = getattr(deployed_contract.functions, func_name)(*args).call()
        return result

    def get_contract_addr(self):
        self.tx_receipt = web3.eth.waitForTransactionReceipt(self.tx_hash)
        if self.tx_receipt['status'] == 0:
            print("deploy failed!!!")
            assert 0
        self.contract_addr = self.tx_receipt['contractAddress']
        return self.contract_addr


if __name__ == '__main__':
    import os
    acc1 = "0x4d6EceA9a5D386DA89293F9D82508098eFC18d63"
    acc2 = "0xb378f39Ff995F86747Cf1ECb80318AE86eD4Ea9E"
    path = "/home/jk/Documents/json-parser-contract"

    token_contract = MyContract(
        os.path.join(path, "target", "json_parser_contract.wasm"),
        os.path.join(path, "target", "json", "JsonParserInterface.json"),
    )
    tx_hash = token_contract.transact(
        "constructor",
        acc1,
    )
    contract_addr = token_contract.get_contract_addr()
    print(contract_addr)
    print(tx_hash)
    # path = "/home/jk/Documents/json-parser-contract"
    # contract_addr = "0x718c724939C9893Ca8d92C1Da8396906c3221D96"
    # token_contract = MyContract(
    #     os.path.join(path, "target", "json_parser_contract.wasm"),
    #     os.path.join(path, "target", "json", "JsonParserInterface.json"),
    #     contract_addr=contract_addr,
    # )
    # tx_hash = token_contract.transact(
    #     "transfer",
    #     acc1,
    #     acc2,
    #     100
    # )
    # tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    # print(tx_receipt)
    #
    # result = token_contract.call(
    #     "totalSupply",
    #     None
    # )
    # result = token_contract.call(
    #     "balanceOf",
    #     None,
    #     acc1
    # )
    # result = token_contract.call(
    #     "checkString",
    #     None,
    #     "asdf"
    # )
    # result = token_contract.call(
    #     "transfer",
    #     acc1,
    #     acc2,
    #     100
    # )
    with open("test.json", 'r') as f:
        json_str = f.read()
    result = token_contract.call(
        "checkFieldIntegrity",
        None,
        json_str
    )


    print(result)
    # tx_hash = token_contract.transact(
    #     "checkFieldIntegrity",
    #     acc1,
    #     "afsadfa"
    # )
    # tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    # print(tx_receipt)