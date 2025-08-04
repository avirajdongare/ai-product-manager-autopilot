# AI-Powered Product Planning Agent

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
```

## 📈 Use Cases

| Role               | Use Case                                                                 |
|--------------------|--------------------------------------------------------------------------|
| **TPMs / PMs**      | Auto-generate technical project roadmaps from high-level goals           |
| **Startups**        | Bootstrap implementation plans for MVPs                                  |
| **Consultants**     | Create client-ready project plans with deliverables and tech stack       |
| **Engineering Leads** | Auto-create Jira or GitHub issues from planning discussions             |
