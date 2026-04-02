<!-- PROJECT LOGO -->
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Logo" width="120" height="120">
</p>

<h1 align="center">GenAI Recruiter Bot</h1>

<p align="center">
  An AI-powered SMS-style recruiter chatbot that screens Python Developer candidates,<br>
  answers their questions, and schedules interviews through a Streamlit interface.
</p>

---

## Table of Contents

- [About The Project](#about-the-project)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Evaluation](#evaluation)
- [To-Do List](#to-do-list)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

## About The Project

This project is a Proof-of-Concept for an AI-powered recruiter assistant as part of **Generative AI** course by the Technion.  
The bot interacts with job candidates for a **Python Developer** position via a Streamlit chat interface (simulating SMS).

The system orchestrates three specialized AI agents:
- **Exit Advisor** - decides whether to end the conversation (fine-tuned on real labeled data)
- **Scheduling Advisor** - checks available interview slots from a SQL database and books them
- **Information Advisor** - generates quastions and answers to communicate with the candidate

<div style="background: #1e1e2e; color: #cdd6f4; padding: 12px 16px; border-radius: 8px; margin-top: 8px;">
  <b>Technologies:</b> Python · OpenAI API · LangChain · Streamlit · ChromaDB · SQLite · Fine-Tuning · RAG
</div>

---

## Features

- [x] Multi-agent orchestration (Main Agent + 3 Advisors)
- [x] Exit Advisor fine-tuned on labeled conversation data
- [x] RAG-based Information Advisor using ChromaDB + OpenAI Embeddings
- [x] Interview scheduling with live availability from SQLite DB
- [x] Streamlit chat UI with conversation state management
- [x] Evaluation notebook with Accuracy, F1, and Confusion Matrix
- [x] Externalized prompts (`.txt` files) for easy customization
- [x] Swap job positions by replacing a single PDF file
- [ ] Cloud deployment _(coming soon)_

---

## Getting Started

### Prerequisites

- Python >= 3.10
- OpenAI API key
- pip

### Installation

```bash
git clone https://github.com/NoamBroit/GenAI_Final_Project-.git
cd GenAI_Final_Project-

python -m venv .venv-FinalProject
source .venv-FinalProject/Scripts/activate   # Windows
# or
source .venv-FinalProject/bin/activate       # Mac/Linux

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
EXIT_ADVISOR_MODEL=ft:gpt-4o-mini-2024-07-18:personal::DLnxtr15
```

### One-Time Setup

**1. Initialize the database:**

```bash
python -c "from app.Services.db_service import DBService; DBService()"
```

**2. Embed the Job Description into Chroma:**

```bash
python embedding/embed_job_description.py
```

**3. (Optional) Run fine-tuning for ExitAdvisor:**

to be noted that this package already fine tuned. however, a fine tuning script is part of this package for optional use.

```bash
python fine_tuning/prepare_and_finetune.py
```

---

## Usage

### Run the Streamlit app:

```bash
streamlit run streamlit_app/streamlit_main.py
```

### Run evaluation notebook:

Open `test_evals.ipynb` in VS Code or Jupyter and run all cells.

---

## Project Structure

```text
GenAIfinalProject/
├── Advisors/
│   ├── ExitAdvisor/
│   │   ├── ExitAdvisor.py
│   │   └── exit_advisor_prompt.txt
│   ├── InfoAdvisor/
│   │   ├── InfoAdvisor.py
│   │   └── info_advisor_prompt.txt
│   └── SchedulingAdvisor/
│       ├── SchedulingAdvisor.py
│       └── scheduling_advisor_prompt.txt
├── app/
│   ├── agents/
│   │   └── main_agent.py
│   ├── Services/
│   │   ├── db_service.py
│   │   ├── llm_service.py
│   │   ├── pdf_service.py
│   │   └── chroma_service.py
│   └── main.py
├── embedding/
│   ├── embed_job_description.py
│   └── chroma_db/               ← 
├── .env
├── .gitignore
├── db_Tech.sql
├── tech.db
├── requirements.txt
├── sms_conversations.json
├── PythonDeveloperJobDescription.pdf
└── test_evals.ipynb
```

---

## Architecture

```
User (Streamlit)
      │
      ▼
  MainAgent
  ├── ExitAdvisor        → Fine-tuned gpt-4o-mini  → End / Continue
  ├── SchedulingAdvisor  → gpt-4o-mini + SQLite DB  → Schedule / Confirm / None
  └── InfoAdvisor        → gpt-4o-mini + ChromaDB   → Continue conversation
```

**Decision flow per message:**

1. `ExitAdvisor` — should we end the conversation?
2. `SchedulingAdvisor` — is the candidate ready to schedule?
3. `InfoAdvisor` — continue gathering info / answer questions

---

## Evaluation

The `test_evals.ipynb` notebook evaluates the `ExitAdvisor` against the labeled dataset (`sms_conversations.json`).

**Metrics:** Accuracy · Precision · Recall · F1 · Confusion Matrix

To run:
```bash
jupyter notebook test_evals.ipynb
```

---


## Contact

**Noam Broitman** — [noambro@gmail.com](mailto:noambro@gmail.com)

Project Link: [https://github.com/NoamBroit/GenAI_Final_Project-](https://github.com/NoamBroit/GenAI_Final_Project-)

---

## Acknowledgments

- [OpenAI](https://platform.openai.com/)
- [Streamlit](https://streamlit.io/)
- [ChromaDB](https://www.trychroma.com/)
- [LangChain](https://www.langchain.com/)
- [Python](https://www.python.org/)
