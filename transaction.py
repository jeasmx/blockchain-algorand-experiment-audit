from algokit_utils import AlgorandClient, PaymentParams, AssetOptInParams, AssetTransferParams
from algokit_utils.models.amount import AlgoAmount

def main() -> None:
    asset_id = 1055

    print("👋 Starting your transaction...")

    algorand = AlgorandClient.default_localnet()

    josue = algorand.account.from_environment("JOSUE")
    eduardo = algorand.account.from_environment("EDUARDO", AlgoAmount(algo=0))

    print(f"Josue's address: {josue.address}")
    print(f"Eduardo's address: {eduardo.address}")

    # Build Atomic Transaction Group
    group_result = (
        algorand.new_group()
        .add_payment(  # Josue sends 1 ALGO to Eduardo. Try removing this transaction and you'll see that the entire group will fail.
            PaymentParams(
                sender=josue.address,
                receiver=eduardo.address,
                amount=AlgoAmount(algo=1),
            )
        )
        .add_asset_opt_in(  # Eduardo opts into the asset
            AssetOptInParams(
                sender=eduardo.address,
                asset_id=asset_id,
            )
        )
        .add_asset_transfer(  # Josue transfers 100 EAT to Eduardo
            AssetTransferParams(
                sender=josue.address,
                receiver=eduardo.address,
                asset_id=asset_id,
                amount=100_000_000,
            )
        )
        .send()
    )

    print(f"Atomic group confirmed with TxnID: {group_result.tx_ids[0]}")

if __name__ == "__main__":
    main()
