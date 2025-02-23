from aptos_sdk.client import RestClient
from aptos_sdk.account import Account
from config import REWARDS_COLLECTION_ID, APTOS_ADMIN_PRIVATE_KEY
from database import create_document

APTOS_NODE_URL = "https://fullnode.testnet.aptoslabs.com"
aptos_client = RestClient(APTOS_NODE_URL)

admin_account = Account.load_key(APTOS_ADMIN_PRIVATE_KEY)
CONTRACT_OBJECT_ADDR = "0x5fdc878e058451c4e51d393e1aa2c4d719cb42d4b4e0ea8d8523f3072ed4e762"

def mint_tokens(reps: int, user: dict):
    if reps >= 10:
        try:
            payload = {
                "type": "entry_function_payload",
                "function": f"{CONTRACT_OBJECT_ADDR}::FormFitToken::mint_reward",
                "type_arguments": [],
                "arguments": [user["wallet_address"], "100"]
            }
            tx_hash = aptos_client.submit_transaction(admin_account, payload)
            aptos_client.wait_for_transaction(tx_hash)
            reward = create_document(
                REWARDS_COLLECTION_ID,
                {
                    "user_id": user["$id"],
                    "reps_achieved": reps,
                    "tokens": 100,
                    "tx_hash": tx_hash
                }
            )
            return {"status": "success", "tokens": 100, "tx": tx_hash}
        except Exception as e:
            print(f"Aptos error: {e}")
            return {"status": "error", "message": str(e)}
    return {"status": "no_reward"}