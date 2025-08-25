# Rasa X Documentation

## Table of Contents

- [What is Rasa x](#1-what-is-rasa-x)
- [Features](#2-features)
- [Architecture and Components](#3-architecture-and-components)
- [deploy Rasa X](#4-deploy-rasa-x)
- [Rasa Enterprise](#5-rasa-enterprise)
- [References](#6-references)

## 1. What is Rasa X
 Rasa X is a robust tool for managing and improving Rasa-based conversational AI assistants, offering features like conversation review, annotation, and interactive learning to enhance training data and model accuracy. It provides an friendly interface for reviewing user interactions, annotating intents and entities, and deploying assistants into production environments. Designed for collaboration, it simplifies managing multiple model versions and configurations, enabling teams to refine and scale their assistants efficiently.

## 2. Features

- **Conversation Review**: Provides a detailed interface to review user interactions, identify misclassified intents, and analyze conversation flows to enhance assistant performance.  
- **Annotation Tools**: Simplifies tagging intents, extracting entities, and refining training data directly from real conversations, improving model precision and recall.  
- **Interactive Learning**: Enables real-time interaction with the assistant, allowing developers to test, correct, and enhance responses for better contextual understanding.  
- **Model Versioning**: Allows seamless management of multiple model versions, with tools to compare, update, or revert models, ensuring flexibility and consistency.  
- **Production Testing**: Provides a production-like testing environment to validate assistant behavior, identify potential issues, and ensure a smooth user experience.  
- **Team Collaboration**: Facilitates teamwork by offering shared access to conversation reviews, annotations, and model configurations, promoting efficient workflow management.  
- **Analytics and Insights**: Offers visual reports and metrics, such as intent distribution and conversation success rates, to identify patterns and areas for improvement.  
- **Integration with Rasa Open Source**: Fully compatible with Rasa Open Source 3.0 and beyond, leveraging the latest advancements in machine learning pipelines and policies.  

## 3. Architecture and Components
<div style="text-align: center;">
  <img src="images/architecture.png" alt="Alt text" style="width: 50%; height: auto;">
</div>

**The diagram shows three main categories of services: the purple components represent Rasa X Services, the blue components represent Rasa Open Source services, and the red components represent third-party services.**

### Rasa X Services

1. **Rasa X**: The Rasa X backend and frontend. The backend handles storing and retrieving conversation data, training data, and metadata, such as conversation tags and flagged messages, in the Rasa X database. The frontend interacts with the backend via API calls and provides a user interface for managing conversation and training data, including reviewing conversations, annotating data, and managing models.

2. **Event Service**: Consumes conversation event data from the event broker and stores it in the Rasa X database. This ensures that all interaction events are logged and available for review and analysis.

3. **DB Migration Service**: Ensures that the database schema is compatible and up-to-date with the current version of Rasa X. This service runs automatically during upgrades or deployments to handle schema migrations.

### Rasa Open Source Services  

- **Rasa Production (Interaction Environment):**  
  This service is responsible for running the trained model and handling user interactions. It serves as the primary endpoint for Rasa X to test models in a controlled environment.  
  - It processes user inputs, predicts responses, and returns them to the user.
  - Publishes conversation data (events) to the shared **event broker**, enabling Rasa X to visualize and analyze these interactions.

- **Rasa Worker (Training Environment):**  
  This service is dedicated to training and background tasks.  
  - Receives data from Rasa X, such as NLU examples, stories, and configuration settings, to train or fine-tune models.
  - Handles model creation, including NLU training, dialogue training, and cross-validation.
  - Does not handle live interactions or publish events to the broker, ensuring it is isolated from real-time workloads.

- **Assistant in Production:**  
  This is the deployed assistant that interacts with real users in a live production environment.  
  - Runs the trained model to process and respond to user messages.
  - Publishes conversation data (events) to the shared **event broker**, making it possible to review and improve the assistant via Rasa X.
  - Typically deployed independently of the Rasa X infrastructure to ensure isolation and scalability for production traffic.



### Third-Party Services

1. **Event Broker**:
   - Manages the flow of conversation events between Rasa and Rasa X.
   - Common brokers include RabbitMQ and Kafka, which ensure reliable message queuing and delivery.

2. **SQL Database**:
   - Stores critical data such as conversation histories, training data, and metadata.
   - Supports both Rasa Open Source and Rasa X services.

3. **Database Cache**:
   - Enhances database performance by caching frequently accessed data.
   - Reduces latency and improves response times for Rasa X UI interactions.

4. **NGINX**:
   - Acts as a reverse proxy server to manage traffic between users and backend services.
   - Provides load balancing, SSL termination, and improved security for Rasa deployments.

### The Communication Between Rasa X and Rasa Open Source

Rasa Open Source (OS) operates independently, while Rasa X relies on Rasa OS for conversation data handling, model training, and running. The integration between Rasa X and Rasa OS follows a well-defined workflow:

#### Project Integration
- After connecting a Rasa project (from a Git repository) to Rasa X, all project files—such as the domain, configuration, and NLU data—are uploaded to the Rasa X database.

#### Model Training
1. **Data Transfer**: Rasa X sends the uploaded data to the `rasa-worker` environment using Rasa OS APIs.
2. **Model Training**: The `rasa-worker` trains the model and generates a new version based on the provided data.
3. **Model Availability**: Once training is complete, the model is made available for tasks such as interactive learning, testing, and evaluation.

#### Conversation Handling
- The `rasa-production` service is responsible for running the trained model and responding to user messages.
- When a user interacts with the assistant (e.g., via Rasa X or other input channels), `rasa-production` processes the messages, predicts responses, and returns them to the user.
- End user interactions are sent from the production assistant to the event broker, where they are consumed by Rasa X and displayed in the UI.

#### Event Logging
- The `rasa-production` service publishes conversation events (e.g., user messages, bot responses, executed actions) to the event broker.
- Rasa X consumes these events via its event service, storing them in its database for review and analysis.

#### Review and Improvement
1. **Conversation Review**: Rasa X users can review stored conversations, edit intents, add more examples, and correct errors to enhance the bot's performance.
2. **Continuous Improvement**: Updated training data can be used to train a new model via the `rasa-worker`, ensuring continuous improvement of the assistant.

## 4. deploy Rasa X

This guide will help you deploy Rasa X using Kubernetes with Minikube.

### Steps

#### 1. Install `kubectl`
Run the following commands to install `kubectl`, the Kubernetes command-line tool:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
```

#### 2. Install `kind`

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

#### 4. Install `minikube`
To install `minikube`, run:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

#### 5. Install `kubeadm` and `kubelet`
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

#### 6. Install Helm
To install Helm, run:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

#### 7. Start Minikube
Run the following commands to start Minikube:
```bash
sudo usermod -aG docker $USER && newgrp docker
```
```bash
minikube start --driver="docker"
```

#### 8. Start Minikube Dashboard (optional)
In a new terminal, run:

```bash
sudo usermod -aG docker $USER && newgrp docker
```
```bash
minikube dashboard
```

#### 9. Set Up Tunnel for External Access
In a new terminal, run:

```bash
sudo usermod -aG docker $USER && newgrp docker
```
```bash
minikube tunnel
```

#### 10. Create Deployment Namespace for Rasa X
Create a new namespace for Rasa X:

```bash
kubectl create namespace rasax
helm repo add rasa-x https://rasahq.github.io/rasa-x-helm
```

#### 11. Install Rasa X using Helm

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

#### 12. Show Services and External IPs

To view the services and external IPs:

```bash
kubectl -n rasax get services
```

#### 14. Forwarding `rasax-release-rasa-x-rasa-x.rasax.svc:5005` to `http://<Rasa X External IP>:5005`

1. **Edit the `/etc/hosts` File**  
```bash
  sudo nano /etc/hosts
```

2. **Add the Mapping**  
  Add the following line to the first section of the file, replacing `<External Rasa X IP>` with the actual IP address from Step 14:

```bash
  <External Rasa X IP > rasax-release-rasa-x-rasa-x.rasax.svc
```

  **Example:**

```plaintext
  127.0.0.1 localhost
  10.2.1.24 rasax-release-rasa-x-rasa-x.rasax.svc
```

#### 15. Accessing Rasa X

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

## 5. Rasa Enterprise

<div style="text-align: center;">
  <img src="images/rasa-enterprise.png" alt="Alt text" style="width: 60%; height: auto;">
</div>

   Rasa Enterprise is an integrated platform that includes Rasa Open Source, Rasa X, and additional features to address the organizational and technical complexity of running an assistant at enterprise scale.

### Features Exclusive to Rasa Enterprise

- **Role-Based Access Control (RBAC)**  
  Manage user permissions by assigning roles like admin, annotator, or tester. Customize these roles to control who can view or modify different parts of your assistant. 

- **Single Sign-On (SSO)**  
  Allow users to log in using their existing organizational credentials, simplifying access and enhancing security. 

- **Multiple Deployment Environments**  
  Run different versions of your assistant simultaneously in environments such as development, staging, and production. This setup helps in testing and deploying updates without disrupting the live assistant. 

- **Rasa Docker Image with GPU Support**  
  Use Rasa's GPU-enabled Docker images to speed up model training and processing, especially beneficial for large datasets and complex models. 

   Rasa Enterprise also includes flexible support plans, from launch and installation to long-term maintenance and assistance.

## 6. References
- **[Rasa X site](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/)**
- **[Architecture](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/installation-and-setup/architecture)**
- **[Deployment Requirements](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/installation-and-setup/requirements)**
- **[Helm Chart installation](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/installation-and-setup/install/helm-chart-installation/installation)**
- **[Connect Rasa X to Rasa OS](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/installation-and-setup/connect-rasa-to-rasa-x)**
- **[Connect Rasa X to Git](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/installation-and-setup/post-deploy-steps/set-up-ivc)**
- **[User Guide](https://legacy-docs-rasa-x.rasa.com/docs/rasa-x/user-guide/share-assistant)**