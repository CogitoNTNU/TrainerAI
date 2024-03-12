from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

OPENAI_API_KEY: str = "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"
llm = ChatOpenAI(openai_api_key = OPENAI_API_KEY)

client = OpenAI(
  api_key=OPENAI_API_KEY,
)

output_parser = StrOutputParser()
embeddings = OpenAIEmbeddings()
#You are a personal trainer that creates a wide variety in diffrent workouts and workout plans, you output the workouts as a table.

loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)


prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")
document_chain = create_stuff_documents_chain(llm, prompt)


retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain( retriever, document_chain)

response = retrieval_chain.invoke({"input": "How can langsmith help with testing?"})
print(response["answer"])

document_chain = create_stuff_documents_chain(llm, prompt)


