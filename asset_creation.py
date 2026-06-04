from algokit_utils import AlgorandClient, AlgoAmount, AssetCreateParams

def main():
    print("🚀 Creating your asset...")

    algorand = AlgorandClient.default_localnet()

    josue = algorand.account.from_environment("JOSUE", AlgoAmount(algo=100))

    print(f"Josue: {josue.address}")

    result = algorand.send.asset_create(
        AssetCreateParams(
            # Mandatory fields
            sender=josue.address,
            total=1_000_000_000,       # Amount of whole units of the asset
            decimals=6,                # Amount of fractional units of the asset
            default_frozen=False,

            # Optional asset config fields
            asset_name="Experiment Audit Token",
            unit_name="EAT",
            manager=josue.address,
            reserve=josue.address,
            freeze=josue.address,
            clawback=josue.address,
            url="https://algorand.co",
        )
    )

    # Capture the unique asset ID of the asset after it's created
    asset_id = result.asset_id

    print(f"Asset created with ID: {asset_id}")

if __name__ == "__main__":
    main()
