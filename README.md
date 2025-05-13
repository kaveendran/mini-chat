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

5. Run the server:
   ```
   uvicorn app.api.server:app --reload
   ```

## Usage

Once the server is running, you can interact with the chatbot via the API endpoints:
- POST `/chat`: Send a message to the chatbot
- GET `/health`: Check server health 