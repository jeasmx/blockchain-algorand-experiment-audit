import { useState } from "react";
import "./App.css";

function App() {
  const [experimentId, setExperimentId] = useState("");
  const [resultsHash, setResultsHash] = useState("");
  const [throughput, setThroughput] = useState("");
  const [collisions, setCollisions] = useState("");
  const [timestamp, setTimestamp] = useState("");

  const [capturedExperiment, setCapturedExperiment] = useState<any>(null);
  const [backendResponse, setBackendResponse] = useState<any>(null);

  const [summary, setSummary] = useState("");
  const [counter, setCounter] = useState<number | null>(null);

  const [searchExperimentId, setSearchExperimentId] = useState("");
  const [boxExperiment, setBoxExperiment] = useState<any>(null);

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



  const searchExperimentById = async () => {
    const response = await fetch(
      `http://127.0.0.1:5000/experiment/${searchExperimentId}`
    );

    const result = await response.json();

    console.log("Box Storage response:", result);

    setBoxExperiment(result);
  };



  const handleSubmit = async () => {
    const experiment = {
      experimentId,
      resultsHash,
      throughput,
      collisions,
      timestamp,
    };

    console.log("Experiment to register:", experiment);
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
        <h1>
          Experimental Results
          <br />
          Audit System
        </h1>

        <div className="network-banner">
          <strong>Network:</strong> Algorand TestNet
          <br />
          <strong>Application ID:</strong> 763925996
        </div>

        <p className="subtitle">
          Register experimental metadata and verify integrity through blockchain.
        </p>

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

          <button onClick={handleSubmit}>Register Experiment</button>

          <button onClick={loadBlockchainData}>Read The Last Experiment From Blockchain</button>
        </div>

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

        {capturedExperiment && (
          <section className="preview">
            <h2>Captured Experiment Data</h2>
            <pre>{JSON.stringify(capturedExperiment, null, 2)}</pre>
          </section>
        )}

        {backendResponse && (
          <section className="preview">
            <h2>Backend Response</h2>
            <pre>{JSON.stringify(backendResponse, null, 2)}</pre>
          </section>
        )}

        {backendResponse && (
          <button className="secondary-button" onClick={loadBlockchainData}>
            Read From Blockchain
          </button>
        )}

        {boxExperiment && (
          <section className="preview">
            <h2>Experiment Retrieved From Box Storage</h2>

            <pre>{JSON.stringify(boxExperiment, null, 2)}</pre>
          </section>
        )}


        {summary && (
          <section className="preview">
            <h2>Latest Experiment Retrieved From Blockchain</h2>

            <pre>{summary}</pre>
          </section>
        )}


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
