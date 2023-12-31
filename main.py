
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
import os
import openai
from llama_index.llms import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = os.getenv('OPENAI_API_KEY')


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



@app.post("/stream")
async def stream(query: Query):
    # define LLM
    llm = OpenAI(temperature=0, model="gpt-3.5-turbo", max_tokens=1000)
    service_context = ServiceContext.from_defaults(llm=llm, chunk_size=51200)

    documents = SimpleDirectoryReader('data2').load_data()
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    query_engine = index.as_query_engine(similarity_top_k=10)
    query_preamble= "Given the provided product details, recommend several products from the provided data, and describe them, that satisfies the following search query or question: " 
    prompt = query_preamble + query.content
    response = query_engine.query(prompt + ". Now output this data in a numbered list without including 'Product Name' and 'Description' keywords. Then summarize everything at the end.")
    
    return {"response": response}

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    llm = OpenAI(temperature=0, model="gpt-3.5-turbo", max_tokens=1000)
    service_context = ServiceContext.from_defaults(llm=llm, chunk_size=51200)

    documents = SimpleDirectoryReader('data2').load_data()
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    query_engine = index.as_query_engine(similarity_top_k=10)
    response = query_engine.query("what is this about?")
    return {"response": response}
