# Chatbot Service

## Table of content

- [Introduction](#Intro)
- [High Level Design](#HLD)
- [Installation](#INSALL)

  - [Pre-Requisite](#prerq)<br>
  - [Installation setps](#INST) <br>
  - [Required action](#RQAC)<br>
  - [Security Services](#SSR) <br>

- [Releases](#REL)

- [References](#REF)

<a name="Intro"></a>

## Introduction

This project is a conversational AI chatbot built using the Rasa framework. Designed to provide interactive and intelligent responses, the chatbot leverages advanced natural language understanding (NLU) and dialogue management to assist users effectively. It can understand user intents, extract relevant entities, and offer meaningful interactions.

### The chatbot depends on two application (Rasa and Rasa X)

- **Rasa X** : A user-friendly tool to manage and improve Rasa-based chatbots. It allows reviewing conversations, annotating data, and deploying models, making it easier to refine and scale conversational AI assistants.
- **Rasa os** : An open-source framework for building AI-powered chatbots. It provides tools for creating conversational experiences, including intent recognition, entity extraction, and dynamic responses.

<a name="HLD"></a>

## High Level Design

<div style="text-align: center;">
  <img src="https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/img/architecture.png" alt="Alt text" style="width: 50%; height: auto;">
</div>

**The Rasa architecture includes three main service categories:**

#### Rasa X Services:

- Rasa X: Manages conversation and training data with a user-friendly interface for reviewing interactions and deploying models.
- Event Service: Logs conversation events for review and analysis.
- DB Migration Service: Ensures the database is up-to-date during upgrades.

#### Rasa Open Source Services:

- Rasa Production: Handles Rasa X user interactions, processes messages, and logs events.
- Rasa Worker: Dedicated to training models and background tasks.
- Assistant in Production: Processes real user messages in live environments.

#### Third-Party Services:

- Event Broker: Manages event flow between components (e.g., RabbitMQ, Kafka).
- SQL Database: Stores conversation data and training metadata.
- NGINX: Acts as a reverse proxy for secure traffic handling.

These components interact seamlessly to ensure efficient training, deployment, and performance monitoring of Rasa assistants.

[Click here for more details.](https://gitlab.ehs.com.jo/software_projects/chatbot-service/-/tree/upload-rasa-files/Web_Code/rasa_x#3-architecture-and-components)

<a name="INSALL"></a>

## Installation

<a name="prerq"></a>

- ### Pre-Requisite

<a name="INST"></a>

- ### Installation setps

  #### 1. Clone the Repository

  ```bash
  git clone git@gitlab.ehs.com.jo:software_projects/chatbot-service.git
  cd chatbot-service
  ```

  #### 2. Install Docker and docker compose(if not already installed)

  First, remove any existing Docker packages:

  ```bash
  for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
  ```

  Then, install Docker:

  ```bash
  sudo apt-get update
  sudo apt-get install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu   $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \-o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo usermod -aG docker $USER
  ```

  Then log out and log back in to apply the group membership changes

  #### 2. Run docker-compose

  ```bash
  docker-compose up -d
  ```

  #### 3. Add Admin Credential to Rasa X

  ```bash
  docker exec -it rasa_x python /app/scripts/manage_users.py create admin admin123 admin --update
  ```

  #### 4. Accessing Rasa X

  To access Rasa X, follow these steps:

  1. **Access Rasa X app**:

  ```
    http://localhost:5002
  ```

  2. **Login to Rasa X**:

     - Use the following credentials:
       - **Username**: `admin`
       - **Password**: `admin123`

  3. **Connect Rasa X to Git**:

     - Navigate to the **Integrated Version Control** section in Rasa X.
     - Enter your Git repository details and connect it to sync your bot's codebase.

  4. **Train the Chatbot and Activate the Model**:

     - Train a new model in the **Training** section and activate it in the **Models** section.
     - If changes are not reflected, you may need to restart the Rasa OS server.

<a name="RQAC"></a>

- ### Required action
  This part is related to any changes will be applied after apply the installation including Keyes, Menus ,DOW’s Vista Configuration, HL7 Massage’s … etc and it should be written by the related teams (Developer, Integration and BA) .

<a name="SSR"></a>

- ### Security Services
  Optional if needed

<a name="REL"></a>

## Releases

This part will be filled by PLM Team

<a name="REF"></a>

### References

- **[Rasa Open Source](https://rasa.com/docs/rasa/)**
- **[Rasa X](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/)**
