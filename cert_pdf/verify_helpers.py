import json
import requests

from cert_verifier import verifier

# FUNCTION check_confirmation_and_issuer - Check whether the transaction is confirmed 
#                                          and whether the cert is issued by issuer in pubkey_list

def check_confirmation_and_issuer(cert_path, pubkey_list):
    
    ret = dict()
    
    with open(cert_path) as f:
        data = json.load(f)
        chain = data['signature']['anchors'][0]['chain']
        tx_id = data['signature']['anchors'][0] ['sourceId']
        
        if chain == "bitcoinTestnet":
            url = 'https://api.blockcypher.com/v1/btc/test3/txs/'
        elif chain == 'bitcoinMainnet':
            url = 'https://api.blockcypher.com/v1/btc/main/txs/'
        else:
            print('Error - This certificate belongs to neither testnet or mainnet of bitcoin.')
            return

        transaction_data = requests.get(url + tx_id).json()

        try:
            ret['transaction is confirmed'] = transaction_data['confirmations'] > 0
        except Exception as e:
            print(e)
            return

        ret['issued by specific issuer'] = transaction_data['addresses'][0] in pubkey_list

    return ret

def cert_verify(cert_path):
    return verifier.verify_certificate_file(cert_path)