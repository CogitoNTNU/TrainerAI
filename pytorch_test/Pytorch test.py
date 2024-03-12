from openai import OpenAI
from langchain_openai import ChatOpenAI

OPENAI_API_KEY: str = "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"

llm = ChatOpenAI(openai_api_key = OPENAI_API_KEY)
test = llm.invoke("how can langsmith helo with testing?")

client = OpenAI(
  api_key=OPENAI_API_KEY,
)
print(test)

