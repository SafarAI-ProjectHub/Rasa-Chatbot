# 🤖 Chatbot Service (Safar AI – Rasa)

## 📑 Table of Contents
- [Introduction](#introduction)
- [High-Level Design](#high-level-design)
- [Installation Matrix](#installation-matrix)
- [Installation](#installation)
  - [Windows — With Docker](#windows-with-docker)
  - [Windows — Without Docker (Native)](#windows-without-docker-native)
  - [Linux — With Docker](#linux-with-docker)
  - [Linux — Without Docker (Native)](#linux-without-docker-native)
  - [Post-Installation Actions](#post-installation-actions)
  - [Security Considerations](#security-considerations)
- [Releases](#releases)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## 🚀 Introduction
This project is a **conversational AI chatbot** built using the **Rasa framework**, designed for the **Safar AI platform**.  
It provides interactive, intelligent responses by leveraging **Natural Language Understanding (NLU)** and **dialogue management**.  

The chatbot can:  
- Understand **user intents** (e.g., greetings, FAQs, support requests).  
- Extract **entities** (e.g., codes, emails).  
- Provide **context-aware responses** in both **Arabic** and **English**.  

### Components
- **Rasa Open Source (OS)** – Core NLU & dialogue handling engine.  
- **Rasa X** – Management UI for improving training data, testing, and deployment (recommended via Docker).  

---

## 🏗️ High-Level Design
![Rasa Architecture](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/img/architecture.png)

Rasa ecosystem services include **Rasa Production**, **Rasa Worker**, **Rasa X UI**, an **Event Broker** (e.g., RabbitMQ/Kafka), a **SQL DB**, and **NGINX** as a reverse proxy.

---

## 🧭 Installation Matrix
Choose the path that fits your environment and constraints:

| OS      | With Docker (recommended for Rasa X) | Without Docker (native Rasa OS) |
|---------|--------------------------------------|----------------------------------|
| Windows | ✅ Easy (Docker Desktop + Compose)   | ✅ PowerShell + Python venv       |
| Linux   | ✅ Easy (Docker Engine + Compose)    | ✅ Bash + Python venv             |

> **Notes**
> - **Rasa X** is simplest to run via **Docker** on both Windows/Linux.  
> - Native installs are for **Rasa Open Source** (NLU/Core) and actions server.  
> - Recommended Python: **3.8–3.11**. Use a **virtual environment**.

---

## ⚙️ Installation

### Windows (With Docker)
1) **Prerequisites**
- Install **Git** and **Docker Desktop** (enable WSL2 backend).  
- Ensure **docker-compose** is available (built into Docker Desktop).

2) **Clone repo (PowerShell)**
```powershell
git clone https://github.com/SafarAI-ProjectHub/Rasa-Chatbot.git
cd Rasa-Chatbot
```

3) **Start services**
```powershell
docker-compose up -d
```

4) **Create Rasa X admin**
```powershell
docker exec -it rasa_x python /app/scripts/manage_users.py create admin admin123 admin --update
```

5) **Access Rasa X**  
Open: http://localhost:5002  (admin / admin123)

---

### Windows (Without Docker — Native)
> Runs **Rasa Open Source** locally. Rasa X not covered in native Windows here (use Docker for Rasa X).

1) **Install Python & venv**
- Install **Python 3.11** (check “Add Python to PATH”).  
- PowerShell:
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install --upgrade pip
```

2) **Install Rasa & deps**
```powershell
pip install rasa==3.*
pip install rasa-sdk==3.*
```

3) **Train & run**
```powershell
rasa train
rasa run actions  # in a second terminal with venv activated
rasa run --enable-api --cors "*"
# (Optional) test via shell:
# rasa shell
```

---

### Linux (With Docker)
1) **Prerequisites**
- Install **Git**, **Docker Engine**, and **docker compose plugin**.

2) **Clone repo**
```bash
git clone https://github.com/SafarAI-ProjectHub/Rasa-Chatbot.git
cd Rasa-Chatbot
```

3) **Start services**
```bash
docker compose up -d   # or: docker-compose up -d
```

4) **Create Rasa X admin**
```bash
docker exec -it rasa_x python /app/scripts/manage_users.py create admin admin123 admin --update
```

5) **Access Rasa X**  
Open: http://localhost:5002  (admin / admin123)

---

### Linux (Without Docker — Native)
> Runs **Rasa Open Source** and actions locally. Use Docker path for Rasa X.

1) **Install Python & venv**
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

2) **Install Rasa & deps**
```bash
pip install rasa==3.*
pip install rasa-sdk==3.*
```

3) **Train & run**
```bash
rasa train
# Terminal A
rasa run actions
# Terminal B
rasa run --enable-api --cors "*"
# (Optional)
# rasa shell
```

---

### 📝 Post-Installation Actions
- Configure **API Keys**, **Menus**, **HL7 messages**, and other integration settings as required by Safar AI.  
- Define responsibilities across **Development**, **Integration**, and **Business Analysis** teams.

---

### 🔒 Security Considerations
- Use **HTTPS** via NGINX reverse proxy (esp. for Rasa X).  
- Change default **admin** credentials immediately.  
- Enforce **RBAC** in Rasa X.  
- Enable **firewall**, **monitoring**, and secure network policies.

---

## 📦 Releases
- **v1.0.0** – Initial setup with Rasa + Rasa X.  
- **v1.1.0** – Bilingual intents/rules.  
- **v1.2.0 (Planned)** – Safar AI API integrations.

---

## 🛠️ Usage Examples
```bash
# Train
rasa train

# Run bot (Core/HTTP API)
rasa run --enable-api --cors "*"

# Actions server
rasa run actions

# Interactive learning
rasa interactive

# Test
rasa test
```

---

## 🧰 Troubleshooting
- **Actions server not responding** → Ensure `rasa run actions` is running and `endpoints.yml` points to the actions server (default: `http://localhost:5055/webhook`).  
- **CORS errors** → Start Core with `--cors "*"` during development or configure allowed origins.  
- **Model not updating** → Re-run `rasa train`, then restart the core server.  
- **Docker ports in use** → Stop conflicting services or change ports in `docker-compose.yml`.  
- **Python version conflicts** → Use a clean `venv` and ensure Python 3.8–3.11.

---

## 📚 References
- [Rasa Open Source Docs](https://rasa.com/docs/rasa/)  
- [Rasa X Docs](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/)  
- [Docker Engine Install](https://docs.docker.com/engine/install/)  
