# 🛡️ ExpenseShield AI

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security](https://img.shields.io/badge/Security-Guardrails-green.svg)]()

**Secure Multi-Agent Expense Review for Demo and Research**

ExpenseShield AI is a security-focused expense review system that processes expense requests with redaction, policy checks, routing, and report generation. The project is designed for safe demo and research use, with a layered guardrail approach before any decision reaches the model.

## Kaggle Submission Summary

This submission presents a secure, multi-agent expense review system for the Agents for Business track. It combines a coordinator agent with specialized security, finance, and skill agents, exposes a lightweight MCP server for tool-based interaction, and uses reusable agent skills for validation and formatting. A pre-LLM security layer performs PII redaction, prompt injection defense, sandboxed execution, and sanitized reporting before any decision reaches the model.

---

## ✨ Key Features

- 🛡️ **Security Screening** - PII redaction and prompt-injection defense before model processing
- ⚡ **Fast Routing** - Routes low-risk requests quickly and escalates higher-risk cases for review
- 📊 **Policy Checks** - Verifies data integrity and basic corporate-policy conditions
- 📧 **Structured Reporting** - Generates audit-friendly summaries and PDF outputs for reviewed cases
- 🔒 **Pre-Processing Guardrails** - Blocks suspicious inputs before workflow execution
- 📈 **Observability** - Logging and metrics tracking for review and debugging
- 🌐 **Ambient Server** - FastAPI-based event interface for local and demo use
- 🎯 **Human Review** - Manager approval for high-value or sensitive decisions

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Incoming Expense Request                               │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ Orchestrator Agent                                     │
│ Routes the request to specialized agents               │
└───────────────┬───────────────────────┬────────────────┘
                │                       │
                ▼                       ▼
┌───────────────────────┐   ┌────────────────────────────┐
│ Security Agent        │   │ Finance Agent              │
│ PII redaction +      │   │ Risk, policy, and budget  │
│ injection defense     │   │ checks                     │
└──────────┬────────────┘   └────────────┬───────────────┘
           │                              │
           └──────────────┬───────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Skill Agent + Reporting                                │
│ Validations, formatting, PDF, and audit output         │
└─────────────────────────────────────────────────────────┘
```

*Note: The layout reflects the current multi-agent workflow used in the project.*

---

## 📁 Project Structure

```
expense-agent/
├── config.py                    # Global configuration
├── agent.py                     # Main system orchestrator
├── requirements.txt            # Dependencies
├── .env.example                # Sample environment variables
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
├── README.md                    # This file
│
├── ambient/                     # Server layer
│   ├── __init__.py
│   └── fast_api_app.py          # FastAPI endpoints
│
├── security/                    # Security layer
│   ├── __init__.py
│   ├── shield.py                # Master security shield
│   ├── pii_redactor.py          # Personal data protection
│   └── injection_defense.py     # Malicious input prevention
│
├── agents/                      # Multi-agent system
│   ├── __init__.py
│   ├── base_agent.py            # Base agent class
│   ├── orchestrator_agent.py    # Master coordinator
│   ├── security_agent.py        # Security specialist
│   ├── finance_agent.py         # Budget validator
│   └── skill_agent.py           # Dynamic skill loader
│
├── sandbox/                     # Code execution safety
│   ├── __init__.py
│   ├── safe_evaluator.py        # AST-based safety checks
│   └── code_runner.py           # Restricted execution
│
├── workflow/                    # Decision logic
│   ├── __init__.py
│   ├── nodes.py                 # Decision handlers
│   ├── edges.py                 # Routing logic
│   └── graph.py                 # Workflow orchestrator
│
├── database/                    # Data storage
│   ├── __init__.py
│   ├── connection.py            # SQLite connection
│   └── repository.py            # CRUD operations
│
├── notifications/               # Communication
│   ├── __init__.py
│   ├── email_service.py         # SMTP email sender
│   └── pdf_generator.py         # Professional PDF creator
│
├── monitoring/                  # Observability
│   ├── __init__.py
│   ├── logger.py                # Activity logging
│   └── metrics.py               # Performance tracking
│
└── skills/                      # AI capabilities
    ├── __init__.py
    ├── loader.py                # Dynamic skill loader
    ├── git-commit-formatter/
    ├── license-header-adder/
    ├── json-to-pydantic/
    └── database-validator/
```

---

## 🚀 Quick Start

### 1️⃣ Installation

```bash
# Clone the repository
git clone https://github.com/mrmoosaai/expense-agent.git
cd expense-agent

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configuration

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_google_api_key_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@example.com
APP_PASSWORD=your_app_password_here
MANAGER_EMAIL=manager@example.com
AUTO_APPROVE_THRESHOLD=100
```

### 3️⃣ Run the Server

```bash
# Start the FastAPI server
python ambient/fast_api_app.py

# Or use uvicorn directly
uvicorn ambient.fast_api_app:app --host 0.0.0.0 --port 8880 --reload
```

### 4️⃣ Testing the Pub/Sub Endpoint

```bash
# Run the test script
python test_agent.py
```

This sends a low-value expense and a higher-value expense to the local endpoint and prints the responses.

**Alternative with curl (PowerShell):**

```powershell
curl.exe -i -X POST http://localhost:8880/trigger/pubsub `
  -H "Content-Type: application/json" `
  -d '{"message":{"data":"<base64-encoded-json>"}}'
```

---

## 🔒 Security Features

### Multi-Layer Protection

| Layer | Feature | Status |
|-------|---------|--------|
| Input Validation | PII Redaction | ✅ Active |
| Input Validation | Prompt Injection Defense | ✅ Active |
| Processing | Sandbox Execution | ✅ Enabled |
| Output | Secure PDF Generation | ✅ Enabled |
| Audit Trail | Comprehensive Logging | ✅ Active |

### Detected & Protected Against

- Social Security Numbers (SSN)
- Credit Card Numbers
- Phone Numbers
- Email Addresses
- IP Addresses
- Dates of Birth
- Prompt Injection Attacks
- Malicious Code Execution

---

## 📊 Performance Targets

- **Typical processing time**: under 2 seconds for low-risk requests
- **Review coverage**: high-value or suspicious cases are routed for human review
- **Safety posture**: PII is redacted and prompt-injection inputs are blocked before model processing
- **Reporting**: audit-friendly summaries and PDF outputs are generated for reviewed cases

---

## 📧 API Endpoints

### Health Check
```bash
GET /health
```

### Process Expense (Pub/Sub)
```bash
POST /trigger/pubsub
Content-Type: application/json

{
  "message": {
    "data": "base64-encoded-expense-json"
  }
}
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test PII Redaction
python test_pii_simple.py

# Test Injection Defense
python test_injection_defense.py

# Test Agent System
python test_agents_comprehensive.py

# Test PDF Generation
python test_pdf_generator.py

# Full Security Test
python test_security.py

# Final Verification Report
python FINAL_VERIFICATION_REPORT.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mr Moosa AI** - Built for secure demo and research use

- Email: mrmoosaai09@gmail.com
- GitHub: https://github.com/mrmoosaai
- LinkedIn: https://www.linkedin.com/in/mr-moosa-ai-moosa-sohail-khan-b0119440a 
---

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI team for the amazing framework
- The AI agent development community

---

<div align="center">

**⭐ Star this repo if you found it helpful! ⭐**

Made with 🚀 by Mr Moosa AI

**ExpenseShield AI - Secure Multi-Agent Expense Review**

</div>
