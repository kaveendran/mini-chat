# Mini Chat

A minimalistic chatbot using FAISS as a vector database with LLM integration.

## Project Structure

- `app/`: Main application code
  - `api/`: FastAPI server and endpoint definitions
  - `llm/`: Language model integration
  - `vectordb/`: FAISS vector database integration
  - `agents/`: Agentic capabilities
  - `core/`: Core chatbot functionality
- `data/`: Data storage for embeddings and configurations
- `config/`: Configuration files
- `scripts/`: Utility scripts

## Features

- Vector database for efficient retrieval of relevant context
- Email capabilities:
  - Send support queries to the development team
  - Send feature requests and bug reports to the development team
  - Automatic user confirmation emails
- Intent classification for intelligent routing of user queries

## Setup

1. Create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows: `.\.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys and configuration.
   - See `.env-example` for required environment variables
   - Set up email credentials for the email agent functionality

5. Run the server:
   ```
   uvicorn app.api.server:app --reload
   ```

## Usage

Once the server is running, you can interact with the chatbot via the API endpoints:
- POST `/chat`: Send a message to the chatbot
- GET `/health`: Check server health 

## Email Agent

The chatbot includes an email agent that can:

1. Send support queries from users to the development team
2. Send feature requests and bug reports to the development team 
3. Send confirmation emails to users

The email agent will automatically detect when a user message requires email functionality and will:
- Ask for any missing information (name, email, etc.)
- Send appropriate emails based on the context
- Provide confirmations to the user 