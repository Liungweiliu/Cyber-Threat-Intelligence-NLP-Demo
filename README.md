# 🛡️ Cyber Threat Intelligence NLP Demo  
**APT Report Information Extraction & Semantic Retrieval (POC)**  

## 📌 Overview  
This project demonstrates how to use **NLP + LLM + Vector Databases** to automatically extract and retrieve **threat intelligence (Indicators of Compromise, IOCs)** from Advanced Persistent Threat (APT) reports.  
It supports multilingual analysis (English, Chinese, Japanese) and provides a **natural language Q&A interface** to help security analysts quickly access key findings from reports.  

---

## 🎯 Features  
- **APT Report Parsing**: Convert unstructured text into structured data (IP addresses, domains, malware names, MITRE ATT&CK techniques).  
- **Semantic Retrieval**: Search across reports using **HuggingFace embeddings + Vector DB**.  
- **LLM + RAG Pipeline**: Retrieval-Augmented Generation with LangChain to answer natural language queries about reports.  
- **Containerized Deployment**: Docker + Pipenv for reproducible environments.  

---

## 🔧 Tech Stack
```
Models: HuggingFace Transformers (NER, embeddings, summarization)
Pipeline: LangChain (RAG, RetrievalQA)
Vector Database: Qdrant
Infrastructure: Docker, Pipenv
API / UI: FastAPI
```

## 🏗️ Architecture  
```text
[APT Reports] → [Preprocessing] → [HF Transformer NER/Embeddings]
     → [Vector DB: Qdrant] → [LangChain RAG Pipeline]
     → [FastAPI] → [User Query & Threat Intel Retrieval]
```

## 📂 Project Structure
```
cyber-threat-intel-nlp/
│── data/                # APT reports (sample text/PDFs)
│── notebooks/           # Prototypes & EDA
│── src/
│   ├── ingestion/       # Data loaders
│   ├── preprocessing/   # Cleaning & tokenization
│   ├── models/          # HuggingFace models
│   ├── retrieval/       # LangChain + VectorDB pipeline
│   ├── api/             # FastAPI/Gradio demo services
│── docker/              # Dockerfile & docker-compose
│── Pipfile              # Pipenv environment
│── README.md
```


## 🚀 Getting Started
```
# Create environment
pipenv install

# Build & run with Docker
docker-compose up --build

# Launch API demo
uvicorn src.api.app:app --reload
```

## 💡 Roadmap
```
 Add automatic MITRE ATT&CK technique mapping
 Expand multilingual support (EN / ZH / JA)
 Build threat graph for entity linking
 Integrate with open CTI feeds
```

## 📜 Disclaimer
```
This project is for research and educational purposes only.
Data sources are publicly available APT reports.
It is not intended for offensive use or penetration testing.
```