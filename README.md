# Blockchain-Based Experimental Results Audit System

## Project Overview

This project implements a decentralized application (DApp) for auditing and verifying experimental results using the Algorand blockchain. The system allows researchers to register experiment metadata, store cryptographic evidence of generated results, and retrieve records in a transparent and immutable manner.

The application was developed as part of a blockchain course project and is intended to demonstrate how blockchain technology can improve integrity, traceability, and reproducibility in scientific experimentation.

Although the current implementation uses manually entered test data, the system is designed to support future integration with experimental results generated from Slotted ALOHA simulations and machine learning models.

---

## Motivation

Research experiments often generate datasets and performance metrics that must remain trustworthy and verifiable. Traditional storage systems can be modified without leaving evidence of changes.

This project addresses that challenge by storing experiment metadata and result hashes on the Algorand blockchain. Any future modification of the original files would produce a different hash, allowing integrity verification.

The system provides:

- Immutable experiment registration
- Blockchain-based auditability
- Integrity verification through hashes
- Historical record retrieval using Box Storage

---

## System Architecture

```text
React Frontend
        |
        v
Flask Backend
        |
        v
ExperimentAudit Smart Contract
        |
        v
Algorand TestNet
   |             |
   v             v
Global State   Box Storage
```

### Components

#### Frontend

A React-based web interface that allows users to:

- Register experiment metadata
- Query blockchain information
- Search experiments by identifier
- Display blockchain transaction evidence

#### Backend

A Flask REST API responsible for:

- Receiving frontend requests
- Interacting with Algorand
- Calling smart contract methods
- Returning blockchain responses

#### Smart Contract

The ExperimentAudit smart contract stores:

- Experiment identifiers
- Result hashes
- Throughput values
- Collision statistics
- Timestamps
- Blockchain metadata

#### Blockchain Layer

Algorand TestNet provides:

- Immutable storage
- Transaction verification
- Global state management
- Box Storage persistence

---

## Features

### Experiment Registration

The system registers:

- Experiment ID
- Results Hash
- Throughput
- Collisions
- Timestamp

### Blockchain Evidence

Each registration generates:

- Transaction ID
- Application ID
- Blockchain confirmation

### Global State Queries

The smart contract exposes:

- Total experiment counter
- Latest experiment summary
- Last blockchain round
- Last author

### Box Storage Queries

Experiments can be retrieved individually using their Experiment ID.

### TestNet Deployment

The application is deployed and tested on Algorand TestNet.

**Application ID:** `763925996`

---

## Smart Contract Design

### register_experiment()

Stores experiment metadata and creates a Box Storage record.

**Parameters:**

- experiment_id
- results_hash
- throughput
- collisions
- timestamp

**Actions:**

- Updates Global State
- Increments experiment counter
- Stores metadata in Box Storage
- Records blockchain author and round

### get_experiment_summary()

Returns a summary of the latest registered experiment.

### get_experiment_box()

Retrieves a specific experiment using its identifier from Box Storage.

### get_counter()

Returns the total number of registered experiments.

### get_last_round()

Returns the blockchain round associated with the latest registration.

### get_last_author()

Returns the account that performed the latest registration.

---

## Technologies Used

### Blockchain

- Algorand
- Algorand Smart Contracts
- Box Storage
- Algorand TestNet

### Backend

- Python
- Flask
- AlgoKit Utils

### Frontend

- React
- TypeScript
- Vite

### Development Tools

- AlgoKit
- Git
- GitHub
- Poetry

---

## Running the Application

### Start Backend

```bash
python backend/app.py
```

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

The application will be available at:

```text
http://localhost:5173
```

---

## Deploying to TestNet

Deploy the smart contract using:

```bash
algokit project deploy testnet
```

Ensure that the deployment account contains sufficient TestNet ALGOs.

Current TestNet Application ID:

```text
763925996
```

---

## Example Workflow

### Register Experiment

1. Enter experiment metadata.
2. Click **Register Experiment**.
3. Submit the transaction to Algorand TestNet.
4. Receive a transaction identifier.
5. Store metadata on-chain.

### Read Blockchain Data

1. Click **Read From Blockchain**.
2. Retrieve the latest experiment summary.
3. Display blockchain statistics.

### Search by Experiment ID

1. Enter an Experiment ID.
2. Query Box Storage.
3. Retrieve the stored record.
4. Display the experiment information.
5. Show a message if the record does not exist.

---

## Repository Structure

```text
blockchain-project/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   └── app.py
│
├── smart_contracts/
│   ├── experiment_audit/
│   └── artifacts/
│
├── asset_creation.py
├── transaction.py
├── README.md
├── pyproject.toml
├── poetry.lock
├── .gitignore
└── .env
```

---

## Demonstrated Functionality

The implemented prototype demonstrates:

- Blockchain-based experiment registration
- Immutable storage of experiment metadata
- Cryptographic hash registration
- Retrieval of records from Global State
- Retrieval of records from Box Storage
- Smart contract interaction through a web interface
- Backend integration with Algorand TestNet
- Blockchain transaction evidence generation

---

## Future Work

Future versions of this project will integrate experimental data generated from Slotted ALOHA network simulations and machine learning models.

Additional enhancements may include:

- Automated file hashing
- Wallet-based authentication
- Direct file uploads
- Experiment dashboards
- Advanced search capabilities
- Integration with research workflows

The long-term goal is to create a blockchain-based framework for ensuring integrity, traceability, and reproducibility of networking research experiments.

---

## Author

**Josue Eduardo Arguelles Sedano**

Master's Program in Computer Science and Engineering (PCIC)

National Autonomous University of Mexico (UNAM)

---

## License

This project was developed for educational and research purposes.

## Acknowledgements

See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for details about the tools, frameworks, documentation, and educational resources used during the development of this project.
