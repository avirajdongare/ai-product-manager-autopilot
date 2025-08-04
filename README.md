# 📊 AI-Powered Product Planning Agent

A smart FastAPI-powered application that transforms high-level product goals into detailed, actionable technical project plans using Google's Gemini API. It integrates with **Jira** to auto-create issues, supports **GitHub issue creation**, and can generate downloadable **PDF reports** of the generated tasks.

---

## 🚀 Key Features

- **Natural Language to Roadmap**  
  Simply describe your product goal (e.g., _"Build an AI agent to optimize revenue"_), and this app will generate 6–8 detailed technical tasks with phases, technologies, and deliverables.

- **Google Gemini Integration**  
  Uses `gemini-1.5-flash` for high-quality structured response generation.

- **Jira & GitHub Integration**  
  Automatically pushes generated tasks as issues to your Jira or GitHub project boards.

- **PDF Report Generation**  
  Generates a downloadable PDF report of all project tasks.

- **FastAPI with Swagger UI**  
  A beautiful, interactive API interface to test endpoints live in your browser.

---

## 📸 Live Demo Screenshots

> Replace these image links with your actual GitHub image paths once committed.

### 🎯 Step 1: Enter a Goal in `/react-agent` Endpoint  
![React Agent Input](./screenshots/Screenshot_2025-08-03_at_11.32.00_PM.png)

---

### 🧠 Step 2: AI Generates Detailed, Structured Tasks  
![Response Example](./screenshots/Screenshot_2025-08-03_at_11.32.36_PM.png)

---

### 📎 Step 3: Download Project Plan as a PDF Report  
![Swagger Docs](./screenshots/Screenshot_2025-08-03_at_11.57.59_PM.png)

---

## 🛠️ Technologies Used

- **Backend:** FastAPI
- **LLM:** Gemini 1.5 Flash (`google.generativeai`)
- **Task Models:** Pydantic
- **PDF Reports:** FPDF
- **Project Management:** Jira API, GitHub REST API
- **Other:** Uvicorn, dotenv, asyncio

---

## 🧪 API Endpoints

| Endpoint             | Method | Description                                |
|----------------------|--------|--------------------------------------------|
| `/react-agent`       | POST   | Main goal-to-task breakdown using LLM      |
| `/generate-report`   | POST   | Generates and downloads a PDF project plan |
| `/health`            | GET    | Health check for API readiness             |
| `/`                  | GET    | Root welcome message                       |

---

## 🔄 Example Input (Request Body)

```json
{
  "goal": "Help me build an internal LLM for JP Morgan Bank"
}
