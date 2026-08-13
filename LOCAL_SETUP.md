# Dograh (VoiceOS) - Local Setup & Development Guide

This guide provides step-by-step instructions to set up and run Dograh locally.

---

## Prerequisites

Ensure you have the following installed on your machine:
- **Git** (with submodules enabled)
- **Docker Engine & Docker Compose**
- **Node.js 18+ & npm** (for UI development)
- **Python 3.11+** (for API backend development)

Initialize the Pipecat git submodule:
```bash
git submodule update --init --recursive
```

---

## Port Allocation

To prevent port conflicts with tools such as **Coolify** (which often runs on port `8000`), Dograh's default host port for the backend API is configured to **`8001`**.

| Service | Host Port | Protocol / Description |
| :--- | :--- | :--- |
| **Frontend UI** | `3010` (Docker) / `3000` (Local Dev) | Web application dashboard & workflow editor |
| **Backend API** | **`8001`** | FastAPI endpoints & Swagger docs at `/docs` |
| **PostgreSQL** | `5432` | Containerized database |
| **Redis** | `6379` | Cache & background task queue |
| **MinIO Console** | `9001` | Object storage UI console |
| **MinIO API** | `9000` | S3-compatible audio storage |

---

## Option 1: Quick Run via Docker Compose (Full Stack)

Use this method to quickly launch all services (Database, Redis, Storage, Backend, and Frontend) in Docker containers.

1. **Clone the repository and initialize submodules**:
   ```bash
   git clone https://github.com/dograh-hq/dograh.git
   cd dograh
   git submodule update --init --recursive
   ```

2. **Set up root environment secret** (UTF-8 encoding):
   - *Bash / Git Bash*:
     ```bash
     echo "OSS_JWT_SECRET=super-secret-jwt-key-for-local-dev" > .env
     ```
   - *PowerShell*:
     ```powershell
     Set-Content -Path .env -Value "OSS_JWT_SECRET=super-secret-jwt-key-for-local-dev" -Encoding utf8
     ```

3. **Launch all containers**:
   ```bash
   docker compose up -d
   ```

4. **Access the applications**:
   - **Frontend UI**: [http://localhost:3010](http://localhost:3010) *(or http://localhost:3000 for local dev server)*
   - **Backend API**: [http://localhost:8001](http://localhost:8001)
   - **Swagger Docs**: [http://localhost:8001/docs](http://localhost:8001/docs)
   - **MinIO Console**: [http://localhost:9001](http://localhost:9001) (User: `minioadmin`, Pass: `minioadmin`)

5. **Stop containers**:
   ```bash
   docker compose down
   ```

---

## Option 2: Local Development Setup (Live Code Reloading)

Use this method if you plan to make code changes to the backend or frontend with hot-reloading active.

### Step 1: Start Infrastructure Dependencies (Postgres, Redis, MinIO)

Run the lightweight docker-compose file for infrastructure services only:
```bash
docker compose -f docker-compose-local.yaml up -d
```

### Step 2: Set Up & Run Backend (`api/`)

1. **Copy the Environment Template**:
   - *Linux / macOS / Git Bash*:
     ```bash
     cp api/.env.example api/.env
     ```
   - *Windows (PowerShell)*:
     ```powershell
     Copy-Item api\.env.example api\.env
     ```

2. **Create and Activate a Virtual Environment**:
   - *Linux / macOS*:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r api/requirements.txt
     ```
   - *Windows (PowerShell)*:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     pip install -r api\requirements.txt
     ```

3. **Run Database Migrations**:
   ```bash
   alembic -c api/alembic.ini upgrade head
   ```

4. **Start the Backend Services**:
   - *Linux / macOS*:
     ```bash
     bash scripts/start_services_dev.sh
     ```
   - *Windows (PowerShell)*:
     ```powershell
     .\scripts\start_services_dev.ps1
     ```
   - *Or run uvicorn manually*:
     ```bash
     uvicorn api.app:app --reload --port 8001
     ```

### Step 3: Set Up & Run Frontend (`ui/`)

1. **Copy Environment Template**:
   - *Linux / macOS / Git Bash*:
     ```bash
     cp ui/.env.example ui/.env
     ```
   - *Windows (PowerShell)*:
     ```powershell
     Copy-Item ui\.env.example ui\.env
     ```

2. **Install Dependencies & Start Dev Server**:
   ```bash
   cd ui
   npm install
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Option 3: VS Code Dev Containers

If you use Visual Studio Code:
1. Open the repository root directory in VS Code.
2. Install the **Dev Containers** extension (`ms-vscode-remote.remote-containers`).
3. Press `F1` (or `Ctrl+Shift+P` / `Cmd+Shift+P`) and choose **Dev Containers: Reopen in Container**.
4. Inside the integrated terminal, start the services:
   ```bash
   bash scripts/start_services_dev.sh
   ```
5. In a second terminal tab:
   ```bash
   cd ui && npm run dev
   ```

---

## Useful Development Commands

- **Check backend logs**:
  ```bash
  tail -f logs/latest/*.log
  ```
- **Stop script-managed backend services**:
  ```bash
  bash scripts/stop_services.sh
  ```
- **Run API unit tests**:
  - *Linux / macOS*:
    ```bash
    set -a && source api/.env.test && set +a && python -m pytest api/tests/
    ```
  - *Windows (PowerShell)*:
    ```powershell
    $env:ENVIRONMENT="test"; python -m pytest api/tests/
    ```
