

# 📧 **AI Email Fraud Detection Agent (Google ADK + RAG + Multi-Signal Analysis)**

This project implements a **full AI-powered email fraud and scam detection agent** using **Google’s Agent Development Kit (ADK)** and optional **LangChain/LangGraph** components.  
The system analyzes incoming emails using multiple layers of intelligence:

- **Email content analysis (LLM + RAG)**
- **Sender reputation & domain authentication**
- **URL and webpage phishing inspection**
- **Pattern matching using known scam behaviors**
- **Multi-signal fraud scoring**

This repository contains the complete architecture, tools, agents, and workflow for building a **production-grade fraud analysis system**.

---

# 🚀 **Core Capabilities**
The AI agent performs:

### ✔️ Email Parsing  
Extracts sender, subject, body, headers, and URLs.

### ✔️ Sender Reputation Analysis  
Checks:
- WHOIS domain age  
- SPF/DKIM/DMARC  
- Domain reputation  
- Disposable email domains  

### ✔️ URL & Website Safety Checks  
- Google Safe Browsing  
- Website fetch and HTML inspection  
- Form/login fields detection  
- Suspicious UI patterns  

### ✔️ Email Content Fraud Analysis  
- LLM-based classification  
- RAG-enhanced rule following  
- Social engineering detection  
- Scam template matching  

### ✔️ Final Risk Scoring  
Combines all signals to produce:

- **risk_level** — *Safe / Suspicious / High Risk / Scam*  
- **fraud_score** (0–100)  
- **detailed reasoning**

---

# 📂 **Project Structure**

```
email-fraud-agent/
│
├── agents/
│   ├── email_parser_agent.py
│   ├── sender_reputation_agent.py
│   ├── url_inspector_agent.py
│   ├── content_analysis_agent.py
│   └── decision_agent.py
│
├── tools/
│   ├── whois_tool.py
│   ├── dns_tool.py
│   ├── safe_browsing_tool.py
│   ├── webpage_fetch_tool.py
│   ├── phishing_rules_tool.py
│   ├── rag_retriever.py
│   └── email_parser_tool.py
│
├── rag/
│   ├── knowledge_base/
│   │   ├── fraud_rules.md
│   │   ├── phishing_examples/
│   │   ├── known_scam_domains.txt
│   │   └── email_patterns.md
│   ├── embeddings.py
│   ├── vector_store.py
│   └── ingest.py
│
├── tests/
│   ├── test_email_samples/
│   └── test_agent_pipeline.py
│
├── config/
│   ├── settings.py
│   └── apis.yaml
│
├── main_agent.py
├── requirements.txt
└── README.md
```

---

# 🛠️ **Tools (ADK Functions)**

The system uses modular ADK tools:

### 🔍 **1. WHOIS Lookup**
Returns:
- Domain age  
- Registrar  
- Creation/expiry dates  

### 🌐 **2. DNS Authentication Checks**
Extracts:
- SPF  
- DKIM  
- DMARC  
- Other TXT records  

### 🛡️ **3. Google Safe Browsing Checker**
Checks URLs against Google threat lists.

### 🌐 **4. Webpage Fetcher**
Fetches:
- HTML  
- Website metadata  
- Forms, login pages  
- Suspicious UI patterns  

### 🧪 **5. Phishing Rules Tool**
Provides:
- Regex patterns  
- Keyword-based rules  
- Behavior indicators  

### 📥 **6. Email Parser**
Extracts:
- Sender  
- Subject  
- Body  
- Links  
- Headers  

### 🧠 **7. RAG Retriever**
Retrieves:
- Known scam patterns  
- Prior samples  
- Fraud rules  
- Scam domain lists  

---

# 🤖 **Sub-Agents (ADK Agents)**

Each functional area is handled by a dedicated agent:

### 1️⃣ **EmailParserAgent**  
Parses raw email → structured JSON with sender, body, and extracted URLs.

### 2️⃣ **SenderReputationAgent**  
Analyzes:
- WHOIS age  
- DNS authentication  
- Domain reputation  

Outputs sender credibility + risk signals.

### 3️⃣ **UrlInspectorAgent**  
For each URL found:
- Safe browsing status  
- HTML inspection  
- Phishing indicators  
- Suspicious redirects  

### 4️⃣ **ContentAnalysisAgent**  
LLM + RAG powered fraud reasoning:  
- Scam intent detection  
- Social engineering patterns  
- Rule-matching  
- Scam template similarity  

### 5️⃣ **DecisionAgent**  
Combines ALL signals to compute the final:

- fraud_score (0–100)  
- risk_level  
- classifier explanation  

---

# 🧠 **RAG Implementation**

The system uses Retrieval-Augmented Generation for:

### ✔️ Known scam email examples  
### ✔️ Scam domains  
### ✔️ Fraud rules  
### ✔️ Phishing patterns  
### ✔️ Social engineering indicators  
### ✔️ Brand impersonation patterns  

### **Vector DB Options**
- Chroma  
- Pinecone  
- Weaviate  
- Milvus  

### **RAG Pipeline**
1. Ingest knowledge → embeddings  
2. Store in vector DB  
3. On each email: retrieve similar patterns  
4. LLM reasons using retrieved examples  
5. Produces consistent rule-based fraud evaluation  

---

# 🧬 **ADK Orchestration Flow**

Defined in `main_agent.py`:

```
Parse Email →  
Sender Reputation →  
URL Inspection →  
Content Analysis (LLM + RAG) →  
Decision Agent (Final Score)
```

### Flow Connections:

| From | To |
|------|-----|
| EmailParserAgent | SenderReputationAgent |
| EmailParserAgent | UrlInspectorAgent |
| EmailParserAgent | ContentAnalysisAgent |
| All sub-agents | DecisionAgent |

The DecisionAgent aggregates all signals.

---

# 📊 **Evaluation Metrics**

### Classification Metrics:
- F1 Score  
- Precision  
- Recall  
- ROC-AUC  

### Agent Metrics:
- Tool-calling accuracy  
- URL inspection accuracy  
- RAG recall relevance  
- Consistency across repeated runs  

---

# 📅 **Suggested Roadmap**

### **Day 1 — Setup RAG + Vector DB**
- Create fraud rules  
- Add scam email examples  
- Build embeddings + vector store  

### **Day 2 — Implement Tools**
- WHOIS tool  
- Safe browsing tool  
- DNS checker  
- Webpage analyzer  
- RAG retriever  

### **Day 3 — Implement Sub-Agents + Orchestration**
- Build ADK graph  
- Implement decision agent  
- Run pipeline tests  
- Add sample email test cases  

---

# 📝 **Deliverables**
This project includes:

- Fully structured ADK implementation  
- Modular tools for email + domain + URL analysis  
- Multi-agent architecture  
- RAG knowledge base  
- End-to-end fraud scoring with reasoning  

---

# 📣 **Future Enhancements**
- Automatic real-time IMAP email ingestion  
- Dashboard with fraud trends  
- Integration with VirusTotal API  
- Live phishing domain updates  
- Model fine-tuning with fraud datasets  

---

# ⭐ **Summary**

This system provides a **complete, multi-layered email fraud detection pipeline** powered by:

- **Google ADK**
- **LLMs**
- **RAG**
- **Security tools**
- **Strong rule-based fraud detection**

The architecture is modular, production-ready, and can scale from personal inbox monitoring to enterprise-level fraud analysis.