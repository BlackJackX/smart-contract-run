from web3 import Web3, HTTPProvider
from contract import MyContract

web3 = Web3(HTTPProvider('http://192.168.80.129:8545'))

def constructor(wasm_file, abi_file, account, **kwargs):
    if not kwargs:
        token_contract = MyContract(wasm_file, abi_file)
        tx_hash = token_contract.transact(
            "constructor",
            account,
            1000000
        )
        contract_addr = token_contract.get_contract_addr()
    else:
        token_contract = MyContract(wasm_file, abi_file, **kwargs)
        if token_contract.contract_addr == 0x0:
            contract_addr = token_contract.get_contract_addr()

    return token_contract


def transfer(token_contract, _from, _to, _value):
    tx_hash = token_contract.transact(
        "transfer",
        _from,
        _to,
        100
    )
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

def balance_of(token_contract, account):
    result = token_contract.call(
        "balanceOf",
        None,
        account
    )
    return result

def total_supply(token_contract):
    result = token_contract.call(
        "totalSupply",
        None
    )
    return result

