# !pip install llama-cpp-python

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from llama_cpp import Llama
import uvicorn
import os

app = FastAPI()

# Simple authentication using a predefined token
security = HTTPBearer()
VALID_TOKEN = os.getenv("API_TOKEN", "your-secret-token-here")  # Change this to a secure token

def validate_credentials(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return credentials

# Initialize the model globally
llm = None

def initialize_model():
    global llm
    if llm is None:
        llm = Llama.from_pretrained(
            repo_id="bartowski/Qwen2.5-Coder-0.5B-Instruct-abliterated-GGUF",
            filename="Qwen2.5-Coder-0.5B-Instruct-abliterated-Q3_K_L.gguf",
        )

# Initialize model on startup
@app.on_event("startup")
def startup_event():
    initialize_model()

@app.get("/")
def greet_json():
    return {"Hello": "World!"}

@app.post("/chat")
def chat_completion(prompt: str = "No input example has been defined for this model task.",
                   credentials: HTTPAuthorizationCredentials = Depends(validate_credentials)):
    # Ensure model is initialized
    initialize_model()

    response = llm.create_chat_completion(
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response

if __name__ == "__main__":
    # This allows the app to be run directly and be accessible externally
    import os
    port = int(os.environ.get("PORT", 10000))  # Default to Render's standard port
    uvicorn.run(app, host="0.0.0.0", port=port)