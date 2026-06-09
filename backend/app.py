import sys
from pathlib import Path
from dotenv import load_dotenv

# Carga variables de entorno desde el archivo .env.
# En este proyecto se usa para leer DEPLOYER_MNEMONIC sin escribirlo en el código.
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from algokit_utils import AlgorandClient, AlgoAmount

# Ruta raíz del proyecto.
# Se usa para localizar el cliente Python generado automáticamente por AlgoKit.
ROOT_DIR = Path(__file__).resolve().parent.parent

# Agrega al path de Python la carpeta donde se encuentra el cliente generado
# para el smart contract ExperimentAudit.
sys.path.append(str(ROOT_DIR / "smart_contracts" / "artifacts" / "experiment_audit"))

from experiment_audit_client import ExperimentAuditClient  # noqa: E402

# App ID del smart contract desplegado en Algorand TestNet.
APP_ID = 763925996  # Cambias por el App ID real

# Inicializa la aplicación Flask.
app = Flask(__name__)

# Habilita CORS para permitir peticiones desde el frontend React
# que corre en http://localhost:5173.
CORS(app)


def get_client() -> ExperimentAuditClient:
    """
    Crea y devuelve un cliente para interactuar con el smart contract.

    Este cliente usa Algorand TestNet y la cuenta DEPLOYER definida en
    las variables de entorno. La cuenta firma las transacciones enviadas
    al contrato.
    """

    # Cliente de Algorand apuntando a TestNet.
    algorand = AlgorandClient.testnet()

    # Carga la cuenta DEPLOYER desde la variable DEPLOYER_MNEMONIC.
    account = algorand.account.from_environment(
        "DEPLOYER",
    )

    # Cliente generado por AlgoKit para llamar métodos del contrato.
    return ExperimentAuditClient(
        algorand=algorand,
        app_id=APP_ID,
        default_sender=account.address,
        default_signer=account.signer,
    )


@app.route("/register-experiment", methods=["POST"])
def register_experiment():

    """
    Endpoint para registrar un experimento.

    Recibe los datos desde el frontend React, llama al método
    register_experiment() del smart contract y devuelve evidencia de la
    transacción enviada a Algorand TestNet.
    """

    # Datos enviados por el frontend en formato JSON.
    data = request.json

    # Extrae los campos esperados del formulario.
    experiment_id = data.get("experimentId", "")
    results_hash = data.get("resultsHash", "")
    throughput = data.get("throughput", "")
    collisions = data.get("collisions", "")
    timestamp = data.get("timestamp", "")

    # Crea cliente del smart contract.
    client = get_client()

    # Llama al método register_experiment() del contrato.
    result = client.send.register_experiment(
        args=(
            experiment_id,
            results_hash,
            throughput,
            collisions,
            timestamp,
        )
    )


    # Devuelve al frontend el resultado de la operación.
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

    """
    Endpoint para consultar el resumen del último experimento registrado.

    La información proviene del Global State del smart contract.
    """
    client = get_client()


    # Llama al método get_experiment_summary() del contrato.
    result = client.send.get_experiment_summary()

    return jsonify(
        {
            "status": "success",
            "summary": result.abi_return,
        }
    )

@app.route("/counter", methods=["GET"])
def counter():

    """
    Endpoint para consultar el número total de experimentos registrados.

    Este valor se obtiene desde el contador almacenado en Global State.
    """
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

    """
    Endpoint para consultar un experimento específico por ID.

    La búsqueda se realiza en Box Storage usando experiment_id como llave.
    Si la Box existe, se devuelve la información almacenada. Si no existe,
    se responde con un estado not_found.
    """

    client = get_client()

    try:
        # Consulta Box Storage mediante el método get_experiment_box().
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
        # Si el ID no existe en Box Storage, el contrato genera error.
        # El backend lo captura y devuelve una respuesta clara al frontend.
        return jsonify(
            {
                "status": "not_found",
                "message": f"Experiment ID '{experiment_id}' was not found in Box Storage.",
                "experiment_id": experiment_id,
            }
        ), 404

if __name__ == "__main__":
    # Ejecuta el servidor Flask en modo desarrollo.
    app.run(host="127.0.0.1", port=5000, debug=True)


