import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str = os.getenv(key="OPENAI_API_KEY")
LANGSMITH_API_KEY: str = os.getenv(key="LANGSMITH_API_KEY")

if __name__ == "__main__":
    print(f"[INFO] OPENAI_API_KEY: {OPENAI_API_KEY}")
    print(f"[INFO] LANGSMITH_API_KEY: {LANGSMITH_API_KEY}")