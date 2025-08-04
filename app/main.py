import os
import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor
from .models import GoalRequest, TaskItem
from .agent_core import add_github_to_tasks, generate_detailed_tasks, create_fallback_tasks
from .utils import extract_json_from_response
from .agent_core import generate_detailed_tasks, create_fallback_tasks, add_jira_to_tasks
from fastapi.responses import StreamingResponse
from .utils import generate_pdf_report


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "FastAPI server is running", "endpoints": ["/react-agent"], "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "react-agent", "port": 5000}

def run_task_generation_sync(goal: str):
    try:
        print(f"Starting task generation for: {goal}")
        result = generate_detailed_tasks(goal)
        return result
    except Exception as e:
        print(f"Task generation failed: {str(e)}")
        raise e

@app.post("/react-agent")
async def run_agent(req: GoalRequest):
    try:
        print(f"Received request: {req.goal}")
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = await asyncio.wait_for(
                loop.run_in_executor(executor, run_task_generation_sync, req.goal),
                timeout=60.0
            )
        output_str = result.get("output", "")
        cleaned_json = extract_json_from_response(output_str)
        try:
            json_data = json.loads(cleaned_json)
            if isinstance(json_data, dict) and "tasks" in json_data:
                tasks_data = json_data["tasks"]
            elif isinstance(json_data, list):
                tasks_data = json_data
            else:
                raise ValueError("Invalid JSON structure")
            task_items = []
            for i, task in enumerate(tasks_data):
                if isinstance(task, dict):
                    task_items.append(TaskItem(
                        step=task.get("step", f"Step {i+1}"),
                        task=task.get("task", "Task"),
                        description=task.get("description", task.get("task", "Task description")),
                        technologies=task.get("technologies", []),
                        deliverables=task.get("deliverables", []),
                        estimated_time=task.get("estimated_time", "TBD")
                    ))
            if not task_items:
                raise ValueError("No valid tasks found in response")
            add_jira_to_tasks(task_items)
            add_github_to_tasks(task_items)

            return {"tasks": task_items}
        except (json.JSONDecodeError, ValueError):
            fallback_tasks = create_fallback_tasks(req.goal)
            return {"tasks": fallback_tasks, "note": "Generated using intelligent task analysis"}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out. Please try with a simpler goal.")
    except Exception:
        fallback_tasks = create_fallback_tasks(req.goal)
        return {"tasks": fallback_tasks, "note": "Generated using fallback task analysis due to processing error"}

@app.post("/generate-report")
async def generate_report(tasks: list[TaskItem]):
    pdf_bytes = generate_pdf_report(tasks)
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment;filename=project_plan.pdf"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
