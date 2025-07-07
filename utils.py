import os
from dotenv import load_dotenv
import httpx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_ENDPOINT = os.getenv("MISTRAL_ENDPOINT", "https://api.mistral.ai/v1/chat/completions")

from langchain.schema import Document

def load_chunks_from_txt(file_paths):
    """Load and split plain text into chunks for embedding."""

    text_data = TextLoader(file_path=file_paths , encoding='utf-8')
    text = text_data.load()

    # Extract full text
    full_text = "\n".join([doc.page_content for doc in text])

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(full_text)

    # Convert chunks (strings) into Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    return chunks


def embed_chunks_with_faiss(chunks):
    """Create FAISS vector DB from text chunks using HuggingFace embeddings."""
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_texts(chunks, embedding_model)

    return vectordb

def search(query, vectordb, k=4):
    """Search the FAISS vector DB for top-k similar chunks."""
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    results = retriever.get_relevant_documents(query)
    
   # print(results)
    chunks = [doc.page_content for doc in results]
    scores = [doc.metadata.get('score', 0.9) for doc in results]
    return chunks, scores

def query_mistral(context, question):
    """Query the Mistral API with context and user question."""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content":  '''
You are AskAria, an admission assistant for ACEM college.
Your role is to provide accurate, concise, and relevant answers strictly based on the information you have been trained on, without revealing your data sources. 
Always deliver responses in a direct, to-the-point manner that aligns precisely with the user's intent.

Your responsibilities:
- Only answer questions related to ACEM admissions, courses, departments, placements, scholarships, etc.

-If the question is about available branches, departments, or courses, 
then Please list each course or department as a clean markdown table format:

|Department|       Course        |
|          |B.Tech - CSE         | 
|          |B.Tech - CSE - AIML  | 
|          |B.Tech - Mechanical  | 
|          |B.Tech - Civil       | 
|          |B.Tech - ECE         | 
|          |BBA                  | 
|          |BBA (FS&B)           | 
|          |BBA-Digital Marketing| 
|          |BCA                  | 
|          |BCA-Data Science     | 
|          |MBA                  | 



- If the user asks about the **Fee,Fees or fee structure** of a specific course or branch, provide the **fees in a clean markdown table format**.
  Example table format:

Academic Fees :

| SR.NO | FEE HEAD                               | FEE (in Rs.)|
|-------|----------------------------------------|-------------|
| 1.    | Course Fee                             |             |
| 2.    | University Charges (Variable)          |             |
| 3.    | Security Fee (Refundable, Variable)    |             |


Hostel Fee:

| SR.NO | FEE HEAD                    | FEE (in Rs.)|
|-------|-----------------------------|-------------|
| 1.    | Hostel Fee AC               |             |
| 2.    | Hostel Fee NON-AC           |             |
| 3.    | Security Fee (Refundable)   |             |

Transport Fee:

| SR.NO | FEE HEAD      | FEE (in Rs.)    |
|-------|---------------|-----------------|
| 1.    | Transport Fee | As per location |

- If the user asks about the college location, address, or directions, respond with a helpful message and include the official Google Maps link:

https://www.google.com/maps?q=ARAVALI+COLLEGE+OF+ENGINEERING+AND+MANAGEMENT,+Jasana,+Tigaon+Rd,+Neharpar+Faridabad,+Faridabad,+Haryana+121102 

- ⚠ Do **NOT** include fee information in answers unless the user **explicitly asks** for it using words like: "fee", "fees", "fee structure", "cost", "tuition", etc.
- If a user asks something irrelevant, inappropriate, or outside the college admission context, respond with:
  ⚠ Your question appears to be invalid or inappropriate. Please ask queries only related to the college and its admission process.

'''},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    body = {
        "model": "mistral-medium",  # Change to "mistral-small" if needed
        "messages": messages,
        "temperature": 0.5,
        "top_p": 1.0,
        "max_tokens": 500
    }

    try:
        response = httpx.post(MISTRAL_ENDPOINT, headers=headers, json=body, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Mistral API error: {e}"
