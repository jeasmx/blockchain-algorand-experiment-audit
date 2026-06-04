import { useState } from "react";
import "./App.css";

function App() {
  const [experimentId, setExperimentId] = useState("");
  const [resultsHash, setResultsHash] = useState("");
  const [throughput, setThroughput] = useState("");
  const [collisions, setCollisions] = useState("");
  const [timestamp, setTimestamp] = useState("");

  const handleSubmit = () => {
    const experiment = {
      experimentId,
      resultsHash,
      throughput,
      collisions,
      timestamp,
    };

    console.log("Experiment to register:", experiment);
    alert("Experiment data captured successfully!");
  };

  return (
    <main className="app">
      <section className="card">
        <h1>Experimental Results<br />Audit System</h1>

        <p className="subtitle">
          Register experimental metadata and verify integrity through blockchain.
        </p>

        <div className="form">
          <input placeholder="Experiment ID" value={experimentId} onChange={(e) => setExperimentId(e.target.value)} />
          <input placeholder="Results Hash" value={resultsHash} onChange={(e) => setResultsHash(e.target.value)} />
          <input type="number" placeholder="Throughput" value={throughput} onChange={(e) => setThroughput(e.target.value)} />
          <input type="number" placeholder="Collisions" value={collisions} onChange={(e) => setCollisions(e.target.value)} />
          <input type="datetime-local" value={timestamp} onChange={(e) => setTimestamp(e.target.value)} />

          <button onClick={handleSubmit}>Register Experiment</button>
        </div>
      </section>
    </main>
  );
}

export default App;
