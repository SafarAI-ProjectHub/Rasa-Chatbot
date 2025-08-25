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

  #### 2. Install `kubectl`

  Run the following commands to install `kubectl`, the Kubernetes command-line tool:

  ```bash
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
  echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
  kubectl version --client
  ```

  #### 3. Install `kind`

  To install `kind`, run:

  ```bash
  [ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.26.0/kind-linux-amd64
  chmod +x ./kind
  sudo mv ./kind /usr/local/bin/kind
  ```

  #### 4. Install Docker (if not already installed)

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
  ```

  #### 5. Install `minikube`

  To install `minikube`, run:

  ```bash
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
  ```

  #### 6. Install `kubeadm` and `kubelet`

  Install Kubernetes components:

  ```bash
  sudo apt-get update
  curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
  echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
  sudo apt-get update
  sudo apt-get install -y kubelet kubeadm kubectl
  sudo apt-mark hold kubelet kubeadm kubectl
  sudo systemctl enable --now kubelet
  ```

  #### 7. Install Helm

  To install Helm, run:

  ```bash
  curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
  chmod 700 get_helm.sh
  ./get_helm.sh
  ```

  #### 8. Start Minikube

  Run the following commands to start Minikube:

  ```bash
  sudo usermod -aG docker $USER && newgrp docker
  ```

  ```bash
  minikube start --driver="docker"
  ```

  #### 9. Start Minikube Dashboard (optional)

  In a new terminal, run:

  ```bash
  sudo usermod -aG docker $USER && newgrp docker
  ```

  ```bash
  minikube dashboard
  ```

  #### 10. Set Up Tunnel for External Access

  In a new terminal, run:

  ```bash
  sudo usermod -aG docker $USER && newgrp docker
  ```

  ```bash
  minikube tunnel
  ```

  #### 11. Create Deployment Namespace for Rasa X

  Create a new namespace for Rasa X:

  ```bash
  kubectl create namespace rasax
  ```

  #### 12. Install Rasa X using Helm

  Edit the `basic-values.yml` file to set the external Rasa OS worker and production URL (`http://<Your IP address>:5005`):

  ```yaml
  rasa:
    token: "AnotherSecureRandomString"
    versions:
      rasaProduction:
        enabled: false
        external:
          enabled: true
          url: "<Rasa OS address and port>"
      rasaWorker:
        enabled: false
        external:
          enabled: true
          url: "<Rasa OS address and port>"
  ```

  then run

  ```bash
  helm --namespace rasax install --values rasa_x/charts/basic-values.yml rasax-release rasa-x/rasa-x
  ```

  #### 13. Install Python 3.9 and Rasa (Skip if you want to use Docker)

  To install Python 3.9:

  ```bash
  sudo apt update
  sudo apt install software-properties-common
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt install python3.9
  sudo apt install python3-pip python3.9-dev python3.9-venv
  python3 --version
  pip3 --version
  ```

  To install Rasa, create a virtual environment and install Rasa:

  ```bash
  python3.9 -m venv ./venv
  source ./venv/bin/activate
  pip3 install -U pip
  pip3 install rasa==3.1.7
  python3 -m pip install PyMySQL
  pip3 install websockets==10.4
  ```

  #### 14. Show Services and External IPs

  To view the services and external IPs:

  ```bash
  kubectl -n rasax get services
  ```

  #### 15. Rasa Open Source Configuration

  In `credentials.yml`, modify the Rasa X IP Address:

  ```yaml
  # for the Rasa X "channel", i.e. Talk to your bot and Share with guest testers.
  rasa:
    url: "http://<Rasa X IP Address>:5002/api" # Replace with external Rasa X IP Address from Step 14
  ```

  In `endpoints.yml`, modify the `tracker_store` and `event_broker` and models configurations:

  ```yaml
  model:
    url: http://<Rasa x IP address>:5002/api/models/tag/production # Replace with external Rasa X IP Address from Step 14
    token: "AnotherSecureRandomString" # Use the Rasa X token from basic-values.yml under rasax/charts
    wait_time_between_pulls: 100
  ```

  ```yaml
  tracker_store:
    type: SQL
    dialect: "mysql+pymysql"
    url: "mysql_server_ip_or_hostname" # Replace with your MySQL server IP or hostname
    db: "your_database_name" # Replace with your MySQL database name
    username: "your_username" # Replace with your MySQL username
    password: "your_password" # Replace with your MySQL password

  # Event broker which all conversation events should be streamed to.
  event_broker:
    type: "pika"
    url: "rabbitmq_server_ip_or_hostname" # Replace with external RabbitMQ IP Address from Step 14
    port: "5672"
    username: "user" # Update if RabbitMQ username is customized
    password: "password" # Update if RabbitMQ password is customized
    queues:
      - "rasa_production_events" # Change if using a custom queue name
  ```
  #### 16. Forwarding `rasax-release-rasa-x-rasa-x.rasax.svc:5005` to `http://<Rasa X External IP>:5005`

  #### for local development

  1. **Edit the `/etc/hosts` File**

  ```bash
    sudo nano /etc/hosts
  ```

  2. **Add the Mapping**  
     Add the following line to the first section of the file, replacing `<External Rasa X IP>` with the actual IP address from Step 14:

  ```bash
    <External Rasa X IP> rasax-release-rasa-x-rasa-x.rasax.svc
  ```

      **Example:**

  ```plaintext
    127.0.0.1 localhost
    10.2.1.24 rasax-release-rasa-x-rasa-x.rasax.svc
  ```

  #### for Docker

  Replacing `<External Rasa X IP>` in `docker-compose.yml` with the actual IP address from Step 14:

  ```yaml
  services:
    rasa:
      extra_hosts:
        - "rasax-release-rasa-x-rasa-x.rasax.svc:<External Rasa X IP>"
  ```

  #### 17. Run Rasa

  To run Rasa with images server, run this bash scripts:

  #### for local development

  ```bash
  ./start.sh
  ```

  #### for Docker

  ```bash
  docker-compose -f kubernetes-docker-compose.yml up -d
  ```

  #### 18. Accessing Rasa X

  To access Rasa X, follow these steps:

  1. **Get the External IP**:
     Use the external IP address for the Nginx service retrieved from step 14.

  ```
    http://<Nginx IP address>:8000
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

  5. **Expose Rasa X to Your Local Network (optional)**:

     - To make Rasa X accessible from other devices on your local network, run:

        ```bash
        kubectl port-forward --address 0.0.0.0 -n rasax service/rasax-release-rasa-x-nginx 8080:8000
        ```

     - **If port `8080` is in use**, replace it with another port (e.g., `8081`):

      **Access Rasa X on the Network:**

      - On your machine:  
        `http://localhost:8080`
      
      - From other devices on the same network:  
        `http://<your-local-IP>:8080`  

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
