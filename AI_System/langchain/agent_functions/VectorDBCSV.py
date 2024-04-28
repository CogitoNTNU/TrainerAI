from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="AI_System\langchain\.env")
OPENAI_API_KEY: str = os.getenv(key="OPENAI_API_KEY")

workouts = CSVLoader(file_path="AI_System\langchain\workouts.csv")
loaded_workouts = workouts.load()
embeddings = OpenAIEmbeddings()
faiss = FAISS.from_documents(loaded_workouts, embeddings)  
results = faiss.similarity_search('barbell',2)
print(results)