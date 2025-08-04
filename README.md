# Product Planning AI Agent

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


## 🚀 Running Locally

Follow these steps to get the project up and running on your local machine:

### 1. **Clone the repository**
```bash
git clone https://github.com/avirajdongare/ai-product-manager-autopilot.git
cd ai-product-manager-autopilot
```

##  Running Locally

Follow these steps to get the project up and running on your local machine:

```bash
# 1. Clone the repository
git clone https://github.com/avirajdongare/ai-product-manager-autopilot.git
cd ai-product-manager-autopilot
```

```bash
# 2. Create & activate a virtual environment
python3 -m venv venvpm
source venvpm/bin/activate  # On Windows use: venvpm\Scripts\activate
```

```bash
# 3. Install all dependencies
pip install -r requirements.txt
```

```bash
# 4. Create a .env file in the root directory and add the following:
GEMINI_API_KEY=your_gemini_key_here  
JIRA_API_TOKEN=your_jira_token  
JIRA_EMAIL=your_email@example.com  
JIRA_DOMAIN=yourdomain.atlassian.net  
JIRA_PROJECT_KEY=KAN  
GITHUB_TOKEN=your_github_token  
GITHUB_REPO=your_username/your_repo  
```

```bash
# 5. Run the FastAPI app locally
uvicorn app.main:app --reload --port 5000
```

```bash
# 6. Access Swagger UI
Open your browser and navigate to:
http://127.0.0.1:5000/docs
```
