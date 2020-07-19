from web3 import Web3, HTTPProvider

web3 = Web3(HTTPProvider('http://192.168.80.129:8545'))

def get_accounts():
    accounts = {}
    with open("private_keys", "r") as f:
        for line in f.readlines():
            act = line.split(' ')
            accounts[act[1]] = act[2].rstrip('\n')
    return accounts

def get_coin_from_faucet(_value, _to, _from='0x00a329c0648769A73afAc7F9381E08FB43dBEA72'):

    accounts = get_accounts()

    signed_tx = web3.eth.account.signTransaction(
        dict(
            nonce=web3.eth.getTransactionCount(_from),
            gasPrice=web3.eth.gasPrice,
            gas=100000,
            to=_to,
            value=_value,
            data=b'',
        ),
        accounts[_from],
    )
    return web3.eth.sendRawTransaction(signed_tx.rawTransaction)

def send(_value, _from, _to):

    accounts = get_accounts()

    signed_tx = web3.eth.account.signTransaction(
        dict(
            nonce=web3.eth.getTransactionCount(_from),
            gasPrice=web3.eth.gasPrice,
            gas=100000,
            to=_to,
            value=_value,
            data=b'',
        ),
        accounts[_from],
    )
    return web3.eth.sendRawTransaction(signed_tx.rawTransaction)

if __name__ == "__main__":
    acc1 = "0x4d6EceA9a5D386DA89293F9D82508098eFC18d63"
    acc2 = "0xb378f39Ff995F86747Cf1ECb80318AE86eD4Ea9E"
    # print(send(10000000000000000000, acc1, acc2))
    tx_hash = get_coin_from_faucet(10000000000000000000, acc1)
    print(web3.eth.waitForTransactionReceipt(tx_hash))