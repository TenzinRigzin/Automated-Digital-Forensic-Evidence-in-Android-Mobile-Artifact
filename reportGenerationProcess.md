# 📂 Local Evidence Chatbot & Automated Reporting Suite

A completely secure, private, and local analytics dashboard built with **Python 3.13**, **Streamlit**, and **LangChain**. This system processes your enterprise data locally using vector embeddings, allows you to chat with your records using an ongoing audit-style chatbot, and lets you export findings directly into custom PDF or Excel formats.

---

## 🛠️ Prerequisites

Before launching the system, ensure you have the local LLM server downloaded and running on your machine:
1. Download and install [Ollama](https://ollama.com).
2. Download your preferred analysis engine via your system terminal (this project defaults to Llama 3):
   ```bash
   ollama run llama3
   ```
   *(Ensure the Ollama process remains running in the background).*

---

## 🚀 Step-by-Step Installation Process

Because multiple Python environments can cause pathing conflicts on Windows, execute the commands using the explicit `python -m` prefix to ensure everything maps to your active environment.

### 1. Set Up Your Directory
Navigate to your preferred directory (e.g., your Windows Desktop) where your code script (`app.py`) is located:
```cmd
cd OneDrive\Desktop
```

### 2. Install Core System & AI Dependencies
Install the entire localized suite including UI rendering, PDF/Excel generation modules, and vector math extensions:
```cmd
python -m pip install streamlit reportlab openpyxl langchain langchain-community langchain-chroma langchain-huggingface langchain-ollama sentence-transformers langchain-classic
```

---

## 🎮 How to Run the Application

Launch the local web server directly from your terminal using:
```cmd
python -m streamlit run app.py
```

### What Happens on First Launch:
1. A new browser tab will automatically open at `http://localhost:8501`.
2. The UI will render instantly. A status indicator reading **"Downloading embedding model on first run... Please wait."** will appear. 
3. The system will download a lightweight vector model (`all-MiniLM-L6-v2`) straight to your local hard drive. This happens only **once**.
4. A folder named `./chroma_db` will automatically generate on your Desktop to act as your private local database storage.

---

## 📑 Core Pipeline Architecture

* **Database & Ingestion (`ChromaDB` & `HuggingFace`):** Converts raw multi-format business documents into semantic vector math matrixes stored locally without cloud leakage.
* **Inference Controller (`Ollama`):** Connects LangChain pipelines natively to your machine's hardware to prompt your local LLM with `temperature=0.0` for rigid factual extractions.
* **User Interface (`Streamlit`):** Coordinates ongoing memory threads for standard chat interactions and compiles dynamic document layouts via `ReportLab` and `OpenPyXL`.

---

## 📋 Operational Guide & Exports

* **Chat & Audit:** Use the input field to ask granular questions regarding your data. The model is strictly instructed to return factual citations or reply with "Evidence missing".
* **PDF Export:** Click the **📥 Download PDF Report** button in the sidebar to convert your current analytical session into a clean, markdown-stripped narrative document.
* **Excel Matrix:** Click **📥 Download Excel Spreadsheet** to map out and flatten structural notes directly into cell tracking coordinates.
