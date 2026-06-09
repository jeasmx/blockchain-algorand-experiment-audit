from algopy import ARC4Contract, String, UInt64, Box, Bytes, Global, Txn
from algopy.arc4 import abimethod


class ExperimentAudit(ARC4Contract):
    """
    Smart contract para auditoría de resultados experimentales.

    El objetivo de este contrato es registrar metadatos asociados a
    experimentos y almacenarlos de forma inmutable en la blockchain
    de Algorand.

    Se utilizan dos mecanismos de almacenamiento:

    1. Global State:
       Mantiene un resumen del experimento más reciente y estadísticas
       generales de la aplicación.

    2. Box Storage:
       Permite almacenar y recuperar registros individuales utilizando
       el identificador del experimento como llave.
    """


    def __init__(self) -> None:
        """
        Inicializa el estado global de la aplicación.

        Estas variables permanecen almacenadas en la blockchain y son
        actualizadas cada vez que se registra un nuevo experimento.
        """

        # Número total de experimentos registrados        
        self.experiment_counter = UInt64(0)

        # Información del último experimento registrado
        self.last_experiment_id = String("NONE")
        self.last_results_hash = String("NONE")
        self.last_throughput = String("0")
        self.last_collisions = String("0")
        self.last_timestamp = String("NONE")

        # Información blockchain asociada al último registro
        self.last_author = Bytes(b"")
        self.last_round = UInt64(0)

    @abimethod()
    def hello(self, name: String) -> String:
        """
        Método de ejemplo generado originalmente por AlgoKit.

        Se conserva para validar la comunicación básica con el contrato.
        """
        return String("Hello, ") + name

    @abimethod()
    def register_experiment(
        self,
        experiment_id: String,
        results_hash: String,
        throughput: String,
        collisions: String,
        timestamp: String,
    ) -> String:
        """
        Registra un experimento en la blockchain.

        Parámetros:
        - experiment_id: identificador único del experimento.
        - results_hash: hash criptográfico de los resultados.
        - throughput: métrica de rendimiento obtenida.
        - collisions: número de colisiones observadas.
        - timestamp: fecha y hora asociadas al experimento.

        Este método actualiza el Global State con la información más
        reciente y además crea una entrada permanente en Box Storage.
        """

        # ---------------------------------------------------------
        # Actualizar el resumen global del último experimento
        # ---------------------------------------------------------

        # Incrementar contador total de experimentos
        self.experiment_counter += 1

        # Guardar información del experimento más reciente
        self.last_experiment_id = experiment_id
        self.last_results_hash = results_hash
        self.last_throughput = throughput
        self.last_collisions = collisions
        self.last_timestamp = timestamp

        # Guardar metadatos propios de la blockchain
        self.last_author = Txn.sender.bytes
        self.last_round = Global.round

        # ---------------------------------------------------------
        # Crear una Box asociada al identificador del experimento
        # ---------------------------------------------------------

        # El nombre de la Box será el experiment_id
        box_name = experiment_id.bytes
        experiment_box = Box(Bytes, key=box_name)

        # ---------------------------------------------------------
        # Construir la información que se almacenará en la Box
        # ---------------------------------------------------------

        # Los datos se guardan como una cadena estructurada para
        # facilitar su lectura desde el frontend y backend.
        experiment_data = (
            b"experiment_id="
            + experiment_id.bytes
            + b";hash="
            + results_hash.bytes
            + b";throughput="
            + throughput.bytes
            + b";collisions="
            + collisions.bytes
            + b";timestamp="
            + timestamp.bytes
        )
        # Escribir información en Box Storage
        experiment_box.value = experiment_data

        return String("Experiment registered")

    @abimethod()
    def get_experiment_summary(self) -> String:
        """
        Recupera un resumen del último experimento registrado.

        La información proviene del Global State y permite una consulta
        rápida sin necesidad de acceder a Box Storage.
        """

        return (
            String("Experiment ID: ")
            + self.last_experiment_id
            + String(" | Hash: ")
            + self.last_results_hash
            + String(" | Throughput: ")
            + self.last_throughput
            + String(" | Collisions: ")
            + self.last_collisions
            + String(" | Timestamp: ")
            + self.last_timestamp
        )

    @abimethod()
    def get_experiment_box(
        self,
        experiment_id: String,
    ) -> String:
        """
        Recupera la información completa de un experimento desde
        Box Storage.

        Parámetro:
        - experiment_id: identificador utilizado como llave de búsqueda.
        """

        box_name = experiment_id.bytes
        experiment_box = Box(Bytes, key=box_name)

        return String.from_bytes(experiment_box.value)
        
    @abimethod()
    def get_counter(self) -> UInt64:
        """
        Regresa el número total de experimentos registrados.
        """
        return self.experiment_counter
    
    @abimethod()
    def get_last_round(self) -> UInt64:
        """
        Regresa el número de ronda de Algorand en la que se registró
        el último experimento.
        """
        return self.last_round

    @abimethod()
    def get_last_author(self) -> String:
        """
        Regresa la dirección de la cuenta que realizó el último registro.
        """
        return String.from_bytes(self.last_author)
