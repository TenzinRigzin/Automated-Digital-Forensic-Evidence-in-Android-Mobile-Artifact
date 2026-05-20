# 🚀 Data Indexing, App Execution, and Chronological Logic Guide

This guide details how to load your mobile data files into the local database, run the user interface, and leverage the system's chronological early-stopping capabilities.

---

## 💾 Step 1: Vectorize and Store Your Data
Before starting the chatbot app, you must process the raw logs pulled from your device (e.g., `sms_backup.txt`) into your local database. 

1. Place your extracted text files inside the `data_input` folder on your Desktop.
2. Run the database storage script in your terminal:
   ```cmd
   python index_data.py
   ```
* **Expected Output:** The terminal will display progress logs and end with:  
  `✅ Success! Saved [X] data chunks into local storage.`
* **What happens:** This creates or updates a permanent `./chroma_db` folder on your Desktop containing your data's mathematical meanings.

---

## 🎮 Step 2: Run the Chatbot & Export Dashboard
Once the indexing script reports success, launch the Streamlit graphical user interface:

```cmd
python -m streamlit run app.py
```
* **Interface Access:** A browser tab will automatically open at `http://localhost:8501`. 
* **First Launch Note:** The page will display a status spinner reading *"Downloading embedding model on first run..."* for 1–2 minutes while it builds its local mathematical brain. It will render the chat window immediately afterward.

---

## 🧠 Step 3: Understanding the Chronological Intercept Logic

Standard vector databases sort answers by text relevance, which scrambles chronological timelines and forces the AI to look at random old rows (e.g., Row 2452) out of order. 

To solve this, your `app.py` script runs a custom **Chronological Intercept Engine (`chronological_rag_invoke`)**:

1. **Top-Row Priority:** It intercepts the database results and programmatically moves fragments containing low row indexes (such as Row 1, Row 5, or Line 10) to the absolute top of the pile before handing them to the LLM.
2. **Early Termination (Scanning Break):** If the engine finds matching context within the most recent records (Rows 1–50), it executes a hard `break` in the loop.
3. **Bloat Reduction:** This break drops all remaining database results from the prompt. Older records (like Row 2452) are locked out entirely, preventing unnecessary processing scans and ensuring your answers stay anchored to your latest messages.

---

## 📋 Exporting Your Findings
* Use the chat interface to compile observations, cross-examine evidence, and review timelines.
* Expand the **📋 Export Operations** sidebar.
* Click **📥 Download PDF Report** to convert the session into a clean document, or click **📥 Download Excel Spreadsheet** to flatten the information into structured cells.
