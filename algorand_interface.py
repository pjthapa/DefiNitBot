from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import AssetTransferTxn
import json


def generate_algorand_keypair() -> tuple:
    private_key, address = account.generate_account()
    return private_key, address


def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        client:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if scrutinized_asset['asset-id'] == assetid:
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


def opt_in(account_address, account_key, asset_id):
    """opt in needs to be done on the mainnet"""

    # create the algo client instance
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # OPT-IN

    # Check if asset_id is in account 3's asset holdings prior
    # to opt-in
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    account_info = algod_client.account_info(account_address)
    holding = None
    idx = 0
    for my_account_info in account_info[ 'assets' ]:
        scrutinized_asset = account_info[ 'assets' ][ idx ]
        idx = idx + 1
        if scrutinized_asset[ 'asset-id' ] == asset_id:
            holding = True
            break

    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=account_address,
            sp=params,
            receiver=account_address,
            amt=0,
            index=asset_id)
        stxn = txn.sign(account_key)
        txid = algod_client.send_transaction(stxn)
        # print(txid)
        # Wait for the transaction to be confirmed
        wait_for_confirmation(algod_client, txid, 4)
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        # print_asset_holding(algod_client, account_address, asset_id)


def tip_finite(sender_key, sender: str, account_to_tip: str, asset_id=400593267, tip_amount = 0 ) -> str:
    """
    :param sender_key: private key that needs to be acquired locally
    :param account_to_tip: 10 DefiNite
    :param sender: central account wallet address.
    :param asset_id: pre configured asseet ID for definite
    :return: txid, account_to_tip
    """
    # TRANSFER ASSET
    # create a client on the MainNet
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True
    txn = AssetTransferTxn(
        sender=sender,
        sp=params,
        receiver=account_to_tip,
        amt=tip_amount,
        index=asset_id,
        note="deFinite Tip Bot"
    )
    stxn = txn.sign(sender_key)
    txid = algod_client.send_transaction(stxn)
    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client, txid, 5)
    # The balance should now be 10.
    return txid


