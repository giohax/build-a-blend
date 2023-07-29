
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
import os
import openai
from llama_index.llms import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = os.environ['OPENAI_API_KEY']


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

class Query(BaseModel):
    content: str

# define LLM
llm = OpenAI(temperature=0, model="gpt-3.5-turbo", max_tokens=1000)
service_context = ServiceContext.from_defaults(llm=llm, chunk_size=51200)

documents = SimpleDirectoryReader('data2').load_data()
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
query_engine = index.as_query_engine(
    similarity_top_k=10
)


@app.post("/stream")
async def stream(query: Query):
    query_preamble= "Given the provided product details, recommend several products from the provided data, and describe them, that satisfies the following search query or question: " 
    prompt = query_preamble + query.content
    response = query_engine.query(prompt + ". Now output this data in a numbered list without including 'Product Name' and 'Description' keywords. Then summarize everything at the end.")
    
    return {"response": response}

@app.get("/")
async def main():
    return {"message": "Hello World"}
