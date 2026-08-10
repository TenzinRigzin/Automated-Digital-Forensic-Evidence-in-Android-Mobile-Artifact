import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

INPUT_DIR = "./data_input"
DB_DIR = "./chroma_db"

print("Reading files from data_input folder...")
loader = DirectoryLoader(INPUT_DIR, glob="**/*.*", loader_cls=UnstructuredFileLoader)
raw_documents = loader.load()

if not raw_documents:
    print("❌ No files found! Make sure you dropped your text files or PDFs inside the 'data_input' folder on your Desktop.")
else:
    print(f"📄 Found {len(raw_documents)} file(s). Slicing into text chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(raw_documents)
    
    print("🧠 Converting text into mathematical vector evidence...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("💾 Saving data directly into your local database...")
    vector_store = Chroma.from_documents(docs, embeddings, persist_directory=DB_DIR)
    print(f"✅ Success! Saved {len(docs)} data chunks into local storage.")
