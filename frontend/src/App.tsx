import { useState } from "react";
import "./App.css";

function App() {
  /*
   * Estados del formulario principal.
   * Estos valores representan los metadatos del experimento que el usuario
   * desea registrar en blockchain.
   */
  const [experimentId, setExperimentId] = useState("");
  const [resultsHash, setResultsHash] = useState("");
  const [throughput, setThroughput] = useState("");
  const [collisions, setCollisions] = useState("");
  const [timestamp, setTimestamp] = useState("");

  /*
 * Guarda localmente el experimento capturado desde el formulario.
 * Sirve para mostrar al usuario qué información fue enviada al backend.
 */
  const [capturedExperiment, setCapturedExperiment] = useState<any>(null);

  /*
   * Guarda la respuesta del backend después de registrar un experimento.
   * Aquí se recibe información como App ID, status y Transaction ID.
   */
  const [backendResponse, setBackendResponse] = useState<any>(null);

  /*
 * Estados usados para leer información general desde blockchain.
 * summary contiene el último experimento registrado.
 * counter contiene el número total de experimentos registrados.
 */
  const [summary, setSummary] = useState("");
  const [counter, setCounter] = useState<number | null>(null);

  /*
 * Estados usados para buscar un experimento específico en Box Storage.
 * searchExperimentId almacena el ID a buscar.
 * boxExperiment almacena la respuesta obtenida desde el backend.
 */
  const [searchExperimentId, setSearchExperimentId] = useState("");
  const [boxExperiment, setBoxExperiment] = useState<any>(null);

  /*
 * Consulta información general almacenada en el smart contract.
 *
 * Hace dos peticiones al backend:
 * 1. /summary: obtiene el resumen del último experimento.
 * 2. /counter: obtiene el número total de experimentos registrados.
 */
  const loadBlockchainData = async () => {
    const summaryResponse = await fetch(
      "http://127.0.0.1:5000/summary"
    );

    const summaryData = await summaryResponse.json();

    setSummary(summaryData.summary);

    const counterResponse = await fetch(
      "http://127.0.0.1:5000/counter"
    );

    const counterData = await counterResponse.json();

    setCounter(counterData.counter);
  };


  /*
   * Busca un experimento específico en Box Storage usando su ID.
   *
   * El frontend envía el ID al backend, y el backend llama al método
   * get_experiment_box() del smart contract.
   */
  const searchExperimentById = async () => {
    const response = await fetch(
      `http://127.0.0.1:5000/experiment/${searchExperimentId}`
    );

    const result = await response.json();

    console.log("Box Storage response:", result);

    setBoxExperiment(result);
  };


  /*
   * Envía al backend los datos del experimento capturados en el formulario.
   *
   * El backend recibe estos datos y ejecuta register_experiment() en el
   * smart contract desplegado en Algorand TestNet.
   */
  const handleSubmit = async () => {
    const experiment = {
      experimentId,
      resultsHash,
      throughput,
      collisions,
      timestamp,
    };

    console.log("Experiment to register:", experiment);

    // Guarda una copia local para mostrarla en pantalla.
    setCapturedExperiment(experiment);

    try {
      const response = await fetch("http://127.0.0.1:5000/register-experiment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(experiment),
      });

      const result = await response.json();

      console.log("Backend response:", result);

      // Guarda la respuesta del backend para mostrar evidencia de la transacción.
      setBackendResponse(result);


      alert("Experiment sent to backend successfully!");

    } catch (error) {
      console.error("Error sending experiment:", error);
      alert("Error sending experiment to backend");
    }
  };

  return (
    <main className="app">
      <section className="card">
        {/* Título principal de la DApp */}
        <h1>
          Experimental Results
          <br />
          Audit System
        </h1>

        {/* Muestra explícitamente la red blockchain usada en la demo */}
        <div className="network-banner">
          <strong>Network:</strong> Algorand TestNet
          <br />
          <strong>Application ID:</strong> 763925996
        </div>

        {/* Descripción breve del propósito de la aplicación */}
        <p className="subtitle">
          Register experimental metadata and verify integrity through blockchain.
        </p>

        {/* Formulario principal para registrar experimentos */}
        <div className="form">
          <input
            type="text"
            placeholder="Experiment ID"
            value={experimentId}
            onChange={(e) => setExperimentId(e.target.value)}
          />

          <input
            type="text"
            placeholder="Results Hash"
            value={resultsHash}
            onChange={(e) => setResultsHash(e.target.value)}
          />

          <input
            type="number"
            placeholder="Throughput"
            value={throughput}
            onChange={(e) => setThroughput(e.target.value)}
          />

          <input
            type="number"
            placeholder="Collisions"
            value={collisions}
            onChange={(e) => setCollisions(e.target.value)}
          />

          <input
            type="datetime-local"
            value={timestamp}
            onChange={(e) => setTimestamp(e.target.value)}
          />

          {/* Envía los datos del experimento al backend */}
          <button onClick={handleSubmit}>Register Experiment</button>

          {/* Consulta el último experimento y el contador desde blockchain */}
          <button onClick={loadBlockchainData}>Read The Last Experiment From Blockchain</button>
        </div>

        {/* Sección para buscar un experimento específico en Box Storage */}
        <div className="search-box">
          <input
            type="text"
            placeholder="Experiment ID to search in Box Storage"
            value={searchExperimentId}
            onChange={(e) => setSearchExperimentId(e.target.value)}
          />

          <button onClick={searchExperimentById}>
            Search Experiment in Box Storage
          </button>
        </div>

        {/* Muestra los datos capturados antes de enviarlos a blockchain */}
        {capturedExperiment && (
          <section className="preview">
            <h2>Captured Experiment Data</h2>
            <pre>{JSON.stringify(capturedExperiment, null, 2)}</pre>
          </section>
        )}

        {/* Muestra evidencia de la transacción generada en Algorand TestNet */}
        {backendResponse && (
          <section className="transaction-card">
            <h2>Transaction Submitted Successfully</h2>

            <div className="transaction-row">
              <span>Network</span>
              <strong>Algorand TestNet</strong>
            </div>

            <div className="transaction-row">
              <span>Application ID</span>
              <strong>{backendResponse.app_id}</strong>
            </div>

            <div className="transaction-row">
              <span>Status</span>
              <strong>{backendResponse.status}</strong>
            </div>

            <div className="transaction-row">
              <span>Transaction ID</span>
              <code>{backendResponse.transaction_id}</code>
            </div>
          </section>
        )}



        {/* Muestra el resultado de consultar una Box por Experiment ID */}
        {boxExperiment && (
          <section className="preview">
            <h2>Experiment Retrieved From Box Storage</h2>

            <pre>{JSON.stringify(boxExperiment, null, 2)}</pre>
          </section>
        )}


        {/* Muestra el último experimento recuperado desde Global State */}
        {summary && (
          <section className="preview">
            <h2>Latest Experiment Retrieved From Blockchain</h2>

            <pre>{summary}</pre>
          </section>
        )}


        {/* Muestra el número total de experimentos registrados */}
        {counter !== null && (
          <section className="preview">
            <h2>Blockchain Statistics</h2>

            <p>
              <strong>Total Registered Experiments:</strong> {counter}
            </p>
          </section>
        )}


      </section>
    </main>
  );
}

export default App;
