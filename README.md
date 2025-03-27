# Backend - AI ChatBot

Backend implementation of the AI ChatBot that won the **["24 Heures du Code"](https://les24hducode.fr/)** hackathon.

## 🏆 Objective

The primary goal of the hackathon was to develop a chatbot to automate the reception process at **Hotel California**. Instead of clients having to ask hotel managers for information and make requests manually, they could interact with an AI-powered chatbot that handles basic management tasks seamlessly.

The hackathon organizers provided a pre-developed **REST API** for the Hotel California system. The chatbot's objective was to interpret user requests in natural language and translate them into appropriate API calls.

---

## 🛠️ Application Overview

The chatbot interacts with users via a **frontend UI**, which communicates with the backend using **WebSockets**. The backend processes user messages using the `LangGraph` framework, directing them to an **AI agent** that utilizes predefined tools to execute tasks efficiently.

### 📌 How It Works:
1. **User Input Processing**: Messages are sent to the AI agent.
2. **Tool Invocation**: The AI agent determines the required tools based on the user’s intent.
3. **Parameter Handling**: With the help of `pydantic`, the agent extracts relevant details and fills in missing parameters if possible.
4. **Clarification Requests**: If user input is incomplete or unclear, the agent prompts for missing details.
5. **API Interaction**: The necessary tool sends a request to the **Hotel California REST API**.
6. **Response Handling**: The chatbot displays the API response to the user in the chat.

![Diagram](assets/diagram.png)

### ⬇️ Core Functionalities:
- **Client Management**
- **Restaurant Reservations**
- **Hotel Accommodation Information**
- **Weather Updates**
- **Local Events Lookup**

---

### 🔧 ChatBot Features

✅ **Conversational Memory**: The AI agent retains message history, allowing it to provide context-aware responses.

✅ **Speech Recognition**: Users can interact with the chatbot via voice input.

✅ **Multilingual Support**: The chatbot understands and responds in multiple languages.

---

## 🚀 Run Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/24h-du-code-2025/backend.git <directory>
   ```

2. **Navigate to the repository directory:**
   ```bash
   cd <directory>
   ```

3. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file** using the `.env.dist` template and fill it with environment variables:
   ```ini
   ATLAS_URI=mongodb://127.0.0.1/?retryWrites=true&w=majority
   DB_NAME=hotel-california
   LLM_MODEL=CHATGPT
   HOTEL_API_URL=https://app-584240518682.europe-west9.run.app/
   HOTEL_API_KEY=
   OPEN_WEATHER_API_KEY=
   OPENAI_API_KEY=
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
   LANGSMITH_API_KEY=
   LANGSMITH_PROJECT="hackaton"
   ```

6. **Launch the server:**
   ```bash
   flask --app server run --debug
   ```

   **🔹 Note:** Ensure you have a **MongoDB instance running** on port **27017** before starting the application.

---

## 📁 Project Structure  

| Folder / File | Description |
|--------------|------------|
| [`assets/`](assets) | Application diagrams |
| [`model/`](model) | Model classes for interacting with the hotel REST API |
| [`prompts/`](prompts) | Prompt templates sent to the LLM |
| [`tools/`](tools) | Function tools used by the AI agent |
| [`utils/`](utils) | Utility functions |
| [`config.py`](config.py) | Configuration class storing environment variables |
| [`server.py`](server.py) | Main Flask application |

---

## ⚙️ Technical Stack  

- **🐍 Python** – Core programming language
- **🌶️ Flask** – Web framework
- **🍃 PyMongo** – MongoDB integration
- **🔗 LangChain** – LLM orchestration
- **🕸️ LangGraph** – LLM graph-based reasoning + creation of AI agents
- **📂 LangSmith** – LLM debugging & tracing
- **🤖 OpenAI** – AI model integration
- **🗣️ Whisper** – Speech-to-text processing
