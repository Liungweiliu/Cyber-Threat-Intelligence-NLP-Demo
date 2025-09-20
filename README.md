# 🛡️ Cyber Threat Intelligence NLP Demo  
**APT Report Information Extraction & Semantic Retrieval (POC)**  

## 📌 Overview  
This project demonstrates how to use **NLP + LLM + Vector Databases** to automatically extract and retrieve **threat intelligence (Indicators of Compromise, IOCs)** from Advanced Persistent Threat (APT) reports.  
It provides a **natural language Q&A interface** to help security analysts quickly access key findings from reports.  

---

## 🎯 Features  
- **APT Report Parsing**: Parse JSON-based cyber threat reports and extract metadata from the sigma_analysis_results field (e.g., rule level, source, title, description, author, match context). Store results in a vector database for downstream analysis. 
- **Semantic Retrieval**: Perform semantic search across reports using **HuggingFace embeddings + Qdrant**.  
- **LLM + RAG Pipeline**: Apply LangChain to enable retrieval-augmented QA, answering natural language queries over extracted threat intelligence. 
- **Containerized Deployment**: Reproducible pipeline with Docker + Pipenv, ensuring consistent environments across systems.

---

## 📋 Data Sources

This project leverages publicly available cyber threat intelligence reports to demonstrate information extraction and analysis. The core dataset and Indicators of Compromise (IOCs) used in this demo are derived from a detailed report by **Netskope**, focusing on a specific threat campaign.

Specifically, the analyzed data originates from the following report:

* **"A look at the Nim-based campaign using Microsoft Word docs to impersonate the Nepali government"** from [Netskope Threat Labs](https://www.netskope.com/blog/a-look-at-the-nim-based-campaign-using-microsoft-word-docs-to-impersonate-the-nepali-government)

This approach ensures the project's practicality and relevance by processing real-world, non-offensive threat intelligence for educational and research purposes.

## 🔧 Tech Stack
```
Models: HuggingFace Transformers (embeddings)
Pipeline: LangChain (RAG, RetrievalQA)
Vector Database: Qdrant
Infrastructure: Docker, Pipenv
API / UI: FastAPI
```

## 🏗️ Architecture  
```text
[APT Reports] → [Preprocessing] → [HF Transformer Embeddings]
     → [Vector DB: Qdrant] → [LangChain RAG Pipeline]
     → [FastAPI] → [User Query & Threat Intel Retrieval]
```

## 📂 Project Structure
```
cyber-threat-intel-nlp/
│── data/                # APT reports (json)
│── notebooks/           # Prototypes & EDA
│── src/
│   ├── api/             # FastAPI demo services
│   ├── ingestion/       # Data loaders
│   ├── models/          # HuggingFace models
│   ├── retrieval/       # LangChain + VectorDB pipeline
│── Dockerfile           
│── docker-compose.yml
│── Pipfile              
│── requirements.txt
│── README.md
```


## 🚀 Getting Started
To get the project up and running, follow these steps:
0. **Prepare .env**: First, create a new file named .env in your project's root directory. Copy the contents from .env_sample into .env and fill in the required values for your API keys and service addresses.
1. **Export Dependencies**: Export your Pipenv dependencies to a requirements.txt file. This ensures your Docker build uses the correct package versions.
     ```
     pipenv install
     pipenv shell
     python -um demo ingest_collection
     ```
2. **Build & Run with Docker**: Build the Docker images and start the containers defined in your docker-compose.yml file. This will launch all the services you need.
     ```
     docker-compose up --build
     ```
3. **Access Services**: Once the containers are running, you can access the various services at the following URLs:
     - Jupyter Notebook: http://localhost:8888
     - Qdrant Dashboard: http://localhost:6333/dashboard
     - FastAPI Docs: http://localhost:8000/docs

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
