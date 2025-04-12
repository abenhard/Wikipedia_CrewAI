from dotenv import load_dotenv
from pathlib import Path
import os

# 1. Explicitly load .env file
env_path = Path('..') / '.env'  # Go up one level from tests/ folder
load_dotenv(dotenv_path=env_path)

# 2. Verify loading worked
print("Key exists:", "GROQ_API_KEY" in os.environ)
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY")[:5] + "...")  # Show first 5 chars

# 3. Now import Groq after env is loaded
from langchain_groq import ChatGroq

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL_NAME", "mixtral-8x7b-32768"),
    temperature=0.1
)

response = llm.invoke("Hello world!")
print(response)