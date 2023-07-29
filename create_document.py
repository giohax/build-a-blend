from llama_index import ListIndex, ServiceContext, SimpleKeywordTableIndex, VectorStoreIndex, KnowledgeGraphIndex, StorageContext
import os
import openai
from llama_index.llms import OpenAI
from pathlib import Path
from llama_index import download_loader
import json
from llama_index import Document


os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = os.environ['OPENAI_API_KEY']

# define LLM
llm = OpenAI(temperature=0.5, model="gpt-3.5-turbo", max_tokens=500)
service_context = ServiceContext.from_defaults(llm=llm, chunk_size=51200)


# Open the JSON file
with open('./data/blends.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

documents = []

# Iterate over products
for product in data['products']:
    product_name = product['product_name']
    ingredients = ', '.join(product['ingredients'])
    purpose = ', '.join(product['purpose'])
    
    document_text = (
      f"Product Name: {product_name}\n"
      f"Ingredients: {ingredients}\n"
      f"Purpose: {purpose}\n\n"
    )
    
    document = Document(
        text=document_text
    )
    
    documents.append(document)
    
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

query_engine = index.as_query_engine(
    response_mode="tree_summarize",
    similarity_top_k=3. # since the documents are quite short, we can increase this from the default of 2
)
response = query_engine.query("I need a product for clear skin. ")
print(response) 
