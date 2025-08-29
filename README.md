# 🤖 Chatbot Service (Safar AI – Rasa)

## 📑 Table of Contents
- [Introduction](#introduction)
- [High-Level Design](#high-level-design)
- [Installation](#installation)
  - [Pre-Requisites](#pre-requisites)
  - [Installation Steps](#installation-steps)
  - [Post-Installation Actions](#post-installation-actions)
  - [Security Considerations](#security-considerations)
- [Releases](#releases)
- [Usage Examples](#usage-examples)
- [References](#references)

---

## 🚀 Introduction
This project is a **conversational AI chatbot** built using the **Rasa framework**, designed for the **Safar AI platform**.  
It provides interactive, intelligent responses by leveraging **Natural Language Understanding (NLU)** and **dialogue management**.  

The chatbot can:  
- Understand **user intents** (e.g., greetings, FAQs, support requests).  
- Extract **entities** (e.g., codes, emails).  
- Provide **context-aware responses** in both **Arabic** and **English**.  

### Components:
- **Rasa Open Source (OS)** – Core NLU & dialogue handling engine.  
- **Rasa X** – Management UI for improving training data, testing, and deployment.  

---

## 🏗️ High-Level Design
![Rasa Architecture](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/img/architecture.png)

The Rasa ecosystem consists of three main service categories:

### 1. Rasa X Services
- **Rasa X UI** – Manage conversations, training data, and models.  
- **Event Service** – Logs and stores conversation events.  
- **DB Migration Service** – Keeps the database schema up to date.  

### 2. Rasa Open Source Services
- **Rasa Production** – Processes real user messages.  
- **Rasa Worker** – Handles training and background tasks.  
- **Assistant in Production** – Runs in production environments.  

### 3. Third-Party Services
- **Event Broker** (RabbitMQ/Kafka) – Event streaming.  
- **SQL Database** – Stores training metadata, models, logs.  
- **NGINX** – Reverse proxy for traffic and SSL termination.  

---

## ⚙️ Installation

### 🔑 Pre-Requisites
- Git  
- Docker & Docker Compose  

---

### 📥 Installation Steps

#### 1. Clone the Repository
```bash
git clone git@github.com:SafarAI-ProjectHub/Rasa-Chatbot.git
cd Rasa-Chatbot
```

#### 2. Install Docker & Docker Compose
Remove any old Docker packages:
```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Install dependencies & Docker:
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
# Add Docker’s GPG key & repo
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

(Optional docker-compose binary):
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker $USER
```
👉 Log out/in to apply group membership.

#### 3. Run Services
```bash
docker-compose up -d
```

#### 4. Add Admin User for Rasa X
```bash
docker exec -it rasa_x python /app/scripts/manage_users.py create admin admin123 admin --update
```

#### 5. Access Rasa X
- Open: [http://localhost:5002](http://localhost:5002)  
- Login:  
  - **Username:** `admin`  
  - **Password:** `admin123`  

#### 6. Connect Git
Go to **Integrated Version Control** in Rasa X → Connect your Git repo.

#### 7. Train & Activate Model
- Train in **Training** tab.  
- Activate in **Models** tab.  
- Restart server if needed.

---

### 📝 Post-Installation Actions
- Configure **API Keys**, **Menus**, **HL7 messages**, etc.  
- To be done by Dev, Integration, and BA teams.  

---

### 🔒 Security Considerations
- Use **HTTPS** with NGINX.  
- Change default admin credentials.  
- Enable **role-based access control**.  
- Enable **firewall & monitoring**.  

---

## 📦 Releases
- **v1.0.0** – Initial setup with Rasa + Rasa X.  
- **v1.1.0** – Added bilingual intents/rules.  
- **v1.2.0 (Planned)** – Integration with Safar AI APIs.  

---

## 🛠️ Usage Examples

#### Train the Bot
```bash
rasa train
```

#### Run the Bot in Shell Mode
```bash
rasa shell
```

#### Run Interactive Training
```bash
rasa interactive
```

#### Run Actions Server
```bash
rasa run actions
```

#### Run with API + CORS
```bash
rasa run --enable-api --cors "*"
```

#### Run Tests
```bash
rasa test
```

---

## 📚 References
- [Rasa Open Source Docs](https://rasa.com/docs/rasa/)  
- [Rasa X Docs](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/)  
- [Docker Installation Guide](https://docs.docker.com/engine/install/)  
