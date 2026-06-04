import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from algokit_utils import AlgorandClient, AlgoAmount

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "smart_contracts" / "artifacts" / "experiment_audit"))

from experiment_audit_client import ExperimentAuditClient  # noqa: E402


APP_ID = 763925996  # Cambias por el App ID real

app = Flask(__name__)
CORS(app)


def get_client() -> ExperimentAuditClient:
    algorand = AlgorandClient.testnet()

    account = algorand.account.from_environment(
        "DEPLOYER",
    )

    return ExperimentAuditClient(
        algorand=algorand,
        app_id=APP_ID,
        default_sender=account.address,
        default_signer=account.signer,
    )


@app.route("/register-experiment", methods=["POST"])
def register_experiment():
    data = request.json

    experiment_id = data.get("experimentId", "")
    results_hash = data.get("resultsHash", "")
    throughput = data.get("throughput", "")
    collisions = data.get("collisions", "")
    timestamp = data.get("timestamp", "")

    client = get_client()

    result = client.send.register_experiment(
        args=(
            experiment_id,
            results_hash,
            throughput,
            collisions,
            timestamp,
        )
    )

    return jsonify(
        {
            "status": "success",
            "message": "Experiment registered on Algorand TestNet",
            "app_id": APP_ID,
            "transaction_id": result.tx_ids[0],
            "experiment": data,
        }
    )


@app.route("/summary", methods=["GET"])
def summary():
    client = get_client()

    result = client.send.get_experiment_summary()

    return jsonify(
        {
            "status": "success",
            "summary": result.abi_return,
        }
    )

@app.route("/counter", methods=["GET"])
def counter():
    client = get_client()

    result = client.send.get_counter()

    return jsonify(
        {
            "status": "success",
            "counter": result.abi_return,
        }
    )

@app.route("/experiment/<experiment_id>", methods=["GET"])
def get_experiment(experiment_id):
    client = get_client()

    try:
        result = client.send.get_experiment_box(
            args=(experiment_id,)
        )

        return jsonify(
            {
                "status": "success",
                "experiment_id": experiment_id,
                "box_data": result.abi_return,
            }
        )

    except Exception:
        return jsonify(
            {
                "status": "not_found",
                "message": f"Experiment ID '{experiment_id}' was not found in Box Storage.",
                "experiment_id": experiment_id,
            }
        ), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


