# Rasa OS Documentation

## Table of Contents

- [What is Rasa OS](#1-what-is-rasa-os)
- [Components](#2-components)
- [Features](#3-features)
- [How to Install](#4-how-to-install)
- [File Structure](#5-file-structure)
- [How Rasa works](#6-how-rasa-works)
- [Steps of creating a chatbot](#7-steps-of-creating-a-chatbot)
- [Use Action Server](#8-use-action-server)
- [References](#9-references)

## 1. What is Rasa OS

Rasa is an open-source framework for building conversational AI chatbots and assistants. It provides tools and libraries for developing and deploying AI-driven, text-based chatbots that can handle natural language conversations with users. Rasa enables developers to create interactive and dynamic chatbot experiences that can understand user intents, extract entities, and provide meaningful responses.

## 2. Components

- **Rasa NLU**: This component focuses on understanding and extracting the meaning of user messages. It performs tasks like intent recognition (identifying the user’s intent) and entity recognition (extracting relevant information from the user’s input).
- **Rasa Core**: This component handles the dialogue management of the conversation. It decides how the chatbot should respond based on the user’s input, the context of the conversation, and predefined actions.

## 3. Features

- **Build Stories, Forms, FAQs**
  - **Stories**: Define conversation paths to guide the assistant's behavior based on user inputs.
  - **Forms**: Gather multiple pieces of information from the user in a structured way.
  - **FAQs**: Configure the assistant to answer frequently asked questions using retrieval intents and responses.
- **Extract Entities**: Identify specific pieces of information (e.g., names, dates, locations) from user messages to support conversation goals.
- **Slot Management**: Store extracted data or user-provided information in slots, which influence the conversation flow and responses.
- **Custom Actions**: Use Python to create dynamic actions that fetch data, interact with APIs, or perform custom logic to personalize responses.
- **Interactive Learning**: Train your assistant interactively by testing conversations, refining annotations, and immediately improving the model.
- **Fallback and Error Handling**: Define fallback mechanisms for handling unrecognized inputs or ambiguous user messages to ensure smooth interactions.
- **Multi-language Support**: Train your assistant in multiple languages to cater to diverse user bases, with language-specific NLU pipelines and training data.
- **Context Management**: Use conversation history, slots, and policies to maintain context and provide coherent responses across dialogue turns.
- **Custom NLU Pipelines**: Configure tokenizers, featurizers, classifiers, and entity extractors to suit your assistant's unique requirements.
- **Custom Policies**: Implement dialogue policies like TEDPolicy, RulePolicy, and MemoizationPolicy to control conversation flow and decision-making.
- **Entity Synonyms and Mappings, Regex**: Map different user inputs (e.g., "NYC" and "New York City") to the same entity value and use regex patterns for advanced entity extraction.
- **Integrations**: Seamlessly connect the assistant with channels like WhatsApp, Telegram, Messenger, Slack, or custom web applications.
- **Analytics and Event Tracking**: Monitor conversation logs and events to analyze performance, debug issues, and optimize the assistant over time.

## 4. How to Install

1. Ensure you have Python 3.9 installed or install it using following commands.

  ```bash
    sudo apt update
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.9
    sudo apt install python3-pip python3.9-dev python3.9-venv
    python3 --version
    pip3 --version
  ```

2. Create a virtual environment:
   ```bash
   python3 -m venv rasa-env
   ```
3. Activate the virtual environment:
   ```bash
   source rasa-env/bin/activate
   ```
4. Install Rasa:
   ```bash
   pip3 install -U pip
   pip3 install rasa
   python3 -m pip install PyMySQL
   pip install rasa
   ```
5. Initialize a Rasa project or pull the reposityy:
   ```bash
   rasa init # or pull the repository
   ```

## 5. File Structure

- **domain.yml**: Defines the assistant's knowledge, including intents, entities, slots, responses, forms, and actions.
- **config.yml**: Configures the NLU pipeline and dialogue policies for intent classification and conversation management.
- **data/nlu.yml**: Contains training examples for intents, entities, and FAQs.
- **data/stories.yml**: Defines conversational paths to train the dialogue model.
- **data/rules.yml**: Contains rules for predictable conversation flows, such as form handling or FAQ responses.
  - **_Note that you can crate many nlu files that heve the same structure of the main files._**
- **actions/actions.py**: Contains custom Python actions for dynamic responses and external integrations.
- **tests/test_stories.yml**: Contains end-to-end tests to validate conversation flows and dialogue behavior.
- **credentials.yml**: Configures credentials for connecting the assistant to channels like Slack, Telegram, or Facebook Messenger.
- **endpoints.yml**: Specifies endpoints for custom action servers, trackers, and event brokers like Redis or Kafka.
- **models/**: Stores trained model files for deployment or further testing.

## 6. How Rasa Works

### A- Workflow of Rasa Assistant

#### Step 1: User Input

- The user sends a message via a channel (e.g., WhatsApp, Slack, Webchat).
- The message is passed to the Rasa server.

#### Step 2: Natural Language Understanding (NLU)

- The message is processed by the NLU pipeline defined in `config.yml`.
  - **Tokenizer**: Splits the message into words or tokens (e.g., WhitespaceTokenizer).
  - **Featurizer**: Converts tokens into numerical features for machine learning models (e.g., CountVectorsFeaturizer).
  - **Intent Classifier**: Identifies the user's intent using models like DIETClassifier.
  - **Entity Extractor**: Detects and extracts specific pieces of data (e.g., names, dates, locations) using tools like RegexFeaturizer or Duckling.

#### Step 3: Dialogue Management (Core)

- The **Tracker** records the conversation history and current state (e.g., intents, slots, actions).
- Rasa Core uses the policies to predict the next action:
  - **RulePolicy**: Handles fixed rules for predictable interactions (e.g., FAQs or forms).
  - **TEDPolicy**: Predicts the next action based on the dialogue history and context.
  - **MemoizationPolicy**: Memorizes exact matches of previously seen stories for faster predictions.
- The predicted action could be:
  - Sending a response from `domain.yml`.
  - Triggering a custom Python action.
  - Executing a form or fallback action.

#### Step 4: Action Execution

- If a custom action is required, Rasa communicates with the action server.
- The action server runs Python scripts to fetch external data, call APIs, or manipulate slots.
- The assistant sends the response back to the user.

#### Step 5: Tracker and Event Store

- All events (user messages, actions, and slot updates) are recorded in the Tracker Store for conversation continuity.
- The assistant uses this data to manage context-aware interactions.

### B- Rasa Model Training

### 1. Training the Model

#### a. NLU Training

- **Training Data**: User inputs and Training examples are labeled with **intents** (e.g., `greet`, `ask_doctor`) and **entities** (e.g., `doctor_name`).
- **Pipeline**:  
  The NLU pipeline processes input through several steps:
  - Tokenizes text (splits it into words).
  - Extracts features (e.g., n-grams, regex-based patterns).
  - Uses a **DIETClassifier** (deep learning model) to predict the **intent** and **extract entities**.

#### b. Dialogue Management Training

- **Training Data**: Dialogue is stored as **stories** and **rules**
- **Policies**:  
  The model learns the flow of conversation using:
  - **MemoizationPolicy**: Remembers past actions for repeated scenarios.
  - **TEDPolicy**: Uses deep learning to predict the next action based on conversation history.
  - **RulePolicy**: Follows predefined rules to decide what action to take.

### 2. Using the Trained Model

#### a. Intent Classification

- When the user sends a message, Rasa classifies the **intent** (e.g., `search_doctor`), and extracts any relevant **entities** (e.g., `doctor_name`).

#### b. Dialogue Management

- Rasa uses the conversation context to decide the **next action**:
  - **RulePolicy**: Executes predefined actions.
  - **TEDPolicy**: Predicts the next action based on the conversation flow.

#### c. Response Selection

- **ResponseSelector** picks the best response based on:
  - The intent with the highest confidence.
  - Extracted entities.
  - If necessary, the conversation history.

### 3. Choosing the Closest Match

Rasa selects the best response using:

- **Pattern Matching**: Finds the closest match to user input based on training data.
- **Deep Learning**: The **DIETClassifier** determines the closest intent using learned patterns.
- **Similarity Scoring**: Measures how similar the user input is to training examples, and picks the highest match.

### 4. Action Execution

Once the intent and action are selected:

- Rasa either sends a **response** or performs a **custom action** (e.g., querying a database).
- If more information is needed (e.g., a missing slot), Rasa asks the user for clarification.

## 7. Steps of Creating a Chatbot

The following steps outline how to create a FAQ chatbot using Rasa OS. After installing Rasa OS, follow these steps:

### 1. Define Intents and Add Training Examples in NLU Files

- **What to do**: Define user intents (e.g., `greet`, `faq_delivery`, `faq_payment`) and provide training examples for each intent in the NLU files.
- **File Structure**: Add these examples to `data/nlu.yml`. You can also create multiple NLU files with the same structure.
- **Example**:

  ```yaml
  version: "3.0"
  nlu:
    - intent: greet
      examples: |
        - hello
        - hi
        - hey
        - good morning
        - good evening

    - intent: faq_delivery
      examples: |
        - How long does delivery take?
        - When will my order arrive?
        - Delivery duration?

    - intent: faq_payment
      examples: |
        - What payment methods are available?
        - How can I pay?
        - Do you accept credit cards?
  ```

### 2. Define the Stories and Rules

- **What to do**: Define conversation paths (stories) and rules for specific scenarios.
- **File Structure**: Add these to `data/stories.yml` and `data/rules.yml`.
- **Example Stories**:
  ```yaml
  version: "3.0"
  stories:
    - story: Greet and FAQ
      steps:
        - intent: greet
        - action: utter_greet
        - intent: faq_delivery
        - action: utter_faq_delivery
  ```
- **Example Rules**:
  ```yaml
  version: "3.0"
  rules:
    - rule: Respond to FAQ about delivery
      steps:
        - intent: faq_delivery
        - action: utter_faq_delivery
  ```

### 3. Add Intents, Responses, and Slots/Forms (if applicable) in the Domain File

- **What to do**: Define intents, responses, slots, and forms in `domain.yml`.
- **Example**:

  ```yaml
  version: "3.0"
  intents:
    - greet
    - faq_delivery
    - faq_payment

  responses:
    utter_greet:
      - text: "Hello! How can I assist you today?"
    utter_faq_delivery:
      - text: "Delivery typically takes 3-5 business days."
    utter_faq_payment:
      - text: "We accept credit cards, PayPal, and bank transfers."

  slots:
    user_name:
      type: text
      influence_conversation: false
  ```

### 4. Edit Policies and Pipelines

- **What to do**: Customize the pipeline for intent recognition and entity extraction, and configure dialogue management policies.
- **File**: `config.yml`
- **Example Pipeline**:
  ```yaml
  version: "3.0"
  pipeline:
    - name: WhitespaceTokenizer
    - name: RegexFeaturizer
    - name: LexicalSyntacticFeaturizer
    - name: CountVectorsFeaturizer
      analyzer: "char_wb"
      min_ngram: 1
      max_ngram: 3
    - name: DIETClassifier
      epochs: 100
    - name: EntitySynonymMapper
    - name: ResponseSelector
      epochs: 50
  ```
- **Example Policies**:
  ```yaml
  policies:
    - name: MemoizationPolicy
    - name: RulePolicy
    - name: TEDPolicy
      max_history: 5
      epochs: 50
  ```

### 5. Connect Rasa to a Database Using Tracker Store

- **What to do**: Configure the `tracker_store` in `endpoints.yml` to save conversation data in a database.
- **Example Configuration**:
  ```yaml
  tracker_store:
    type: SQL
    dialect: "mysql+pymysql"
    url: "localhost"
    db: "rasadb"
    username: "root"
    password: ""
  ```
- This ensures that all conversation history is stored for continuity and analysis.

### 6. Test the Chatbot Using Rasa Shell or API

#### Test Locally

1. **Run the Rasa server**:
   ```bash
   ./start.sh
   ```
2. **Test in Rasa Shell**:
   ```bash
   rasa shell
   ```
   Interact with the chatbot in the terminal to ensure it behaves as expected.

#### Test via API

1. **Enable API**:
   Run Rasa with the API enabled:
   ```bash
   rasa run --enable-api
   ```
2. **Send Messages via API**:
   Use `curl` or Postman to test interactions:
   ```bash
   curl -X POST http://localhost:5005/webhooks/rest/webhook \
        -H "Content-Type: application/json" \
        -d '{"sender": "user1", "message": "Hi!"}'
   ```

## 8. Use Action Server

The action server is used to execute custom actions defined in `actions.py`. Here are the steps to run and use it:

### Steps to Run the Action Server

1. **Create the `actions.py` File**:

   - Define custom actions in this file.
   - Example:

     ```python
     from rasa_sdk import Action
     from rasa_sdk.events import SlotSet

     class ActionGetDeliveryInfo(Action):
         def name(self):
             return "action_get_delivery_info"

         def run(self, dispatcher, tracker, domain):
             delivery_info = "Delivery typically takes 3-5 business days."
             dispatcher.utter_message(text=delivery_info)
             return []
     ```

2. **Run the Action Server**:

   - Use the following command to start the action server:
     ```bash
     rasa run actions
     ```

3. **Connect the Action Server**:
   - Ensure the `endpoints.yml` file includes the action server URL:
     ```yaml
     action_endpoint:
       url: "http://localhost:5055/webhook"
     ```

### Steps to Use the Action Server

1. **Define the Custom Action in `domain.yml`**:

   - Example:
     ```yaml
     actions:
       - action_get_delivery_info
     ```

2. **Include the Action in Stories or Rules**:

   - Example:
     ```yaml
     stories:
       - story: Provide delivery info
         steps:
           - intent: faq_delivery
           - action: action_get_delivery_info
     ```

3. **Test the Action**:
   - Run the Rasa server and the action server simultaneously.
   - Use `rasa shell` or API to trigger the action and verify its output.



## 9. References  

### Installation and Setup  
- **[Environment Setup](https://rasa.com/docs/rasa/installation/environment-set-up)** 
- **[Command-Line Interface](https://rasa.com/docs/rasa/command-line-interface)**

### Data Preparation  
- **[Writing Stories](https://rasa.com/docs/rasa/writing-stories/)**
- **[Generating NLU Data](https://rasa.com/docs/rasa/generating-nlu-data/)**
- **[Training Data Format](https://rasa.com/docs/rasa/training-data-format)**
- **[NLU Training Data](https://rasa.com/docs/rasa/nlu-training-data)**  

### Configuration and Customization  
- **[Model Configuration](https://rasa.com/docs/rasa/model-configuration)** 
- **[Actions](https://rasa.com/docs/rasa/actions)**

### Development and Testing  
- **[Conversation-Driven Development](https://rasa.com/docs/rasa/conversation-driven-development/)**

### Architecture and API  
- **[Architecture Overview](https://rasa.com/docs/rasa/arch-overview)** 
- **[HTTP API](https://rasa.com/docs/rasa/http-api)** 
