from deta import Deta  # Import Deta's SDK
from datetime import datetime
from web3 import Web3
import json, os

# Initialize with a Project Key
deta = Deta(os.getenv('DETA_KEY'))

class DBObj(object):
    def __init__(self):
        self.sessions          = deta.Base("sessions")
    
    # def aadhaar_originalsFetch(self, key = None, UID = None):
    #     all_data = []
    #     last = None
    #     while True:
    #         q = {}
    #         if key: q["key"] = key
    #         if UID: q["UID"] = UID
    #         data = self.aadhaar_originals.fetch(q, last=last, limit=10000)
    #         for item in data.items: all_data.append(item)
    #         if data.last is None: break
    #         last = data.last
    #     # sort all_data by addTime
    #     all_data.sort(key = lambda x: datetime.fromisoformat(x["addTime"]))
    #     return all_data

class FileObj(object):
    def __init__(self):
        self.all_files = deta.Drive("all_files")

class DetaObj(object):
    def __init__(self):
        self.db = DBObj()
        self.files = FileObj()

############# Usage #############
deta_obj = DetaObj()




############ CONTRACT - BLOCKCHAIN #################ss
compiled = None
with open("build/contracts/VerifiedHire.json") as f:
    compiled = json.load(f)

web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
blockchain_address_verifiedHire = os.getenv("CONTRACT_ADDRESS_VERIFIED_HIRE")
blockchain = web3.eth.contract(address=blockchain_address_verifiedHire,abi=compiled["abi"])

tx_params = {
    'from': os.getenv("GANACHE_SENDER_ACCOUNT"),
    'gas': 2000000,  # Adjust gas limit as needed
}

def blockChainTransact(t):
    tx_hash = t.transact(tx_params)
    return web3.eth.wait_for_transaction_receipt(tx_hash)
    