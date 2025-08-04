import os
import json
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai
from .models import TaskItem
from .jira_client import create_jira_issue
from .github_client import create_github_issue

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT_TEMPLATE = """
You are an expert AI Product Manager and Technical Architect. Break down the following product goal into 6-8 detailed, actionable tasks.

Goal: {goal}

For each task, include these fields:
- step: The project phase
- task: Brief task title
- description: Specific steps and details
- technologies: List of recommended technologies/tools
- deliverables: List of expected outputs/deliverables
- estimated_time: Time estimate for this task

Respond ONLY with valid JSON in this format:
{{
  "tasks": [
    {{
      "step": "...",
      "task": "...",
      "description": "...",
      "technologies": ["..."],
      "deliverables": ["..."],
      "estimated_time": "..."
    }}
  ]
}}
"""

def generate_detailed_tasks(goal: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(goal=goal)
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=2048
            )
        )
        # Gemini returns text, not a JSON dict
        text = response.text
        return {"output": text}
    except Exception as e:
        print(f"Gemini API failed: {e}")
        return {"output": ""}
    
def add_jira_to_tasks(tasks: List[TaskItem]) -> List[TaskItem]:
    """
    For each relevant technical/dev task, create a Jira ticket and attach the issue key and link.
    """
    jira_phrases = [
        "backend", "development", "api", "technical", "server", 
        "database", "integration", "infrastructure", "deployment"
    ]
    for task in tasks:
        # Check step and task fields for keywords
        task_type = f"{task.step} {task.task}".lower()
        if any(phrase in task_type for phrase in jira_phrases):
            summary = f"{task.step}: {task.task}"
            description = task.description
            issue = create_jira_issue(summary, description)
            if issue:
                task.jira_issue = issue["key"]
                task.jira_link = issue["link"]
            else:
                task.jira_issue = None
                task.jira_link = None
        else:
            task.jira_issue = None
            task.jira_link = None
    return tasks    

def add_github_to_tasks(tasks: List[TaskItem]) -> List[TaskItem]:
    github_phrases = [
        "backend", "development", "api", "technical", "server", 
        "database", "integration", "infrastructure", "deployment"
    ]
    for task in tasks:
        task_type = f"{task.step} {task.task}".lower()
        if any(phrase in task_type for phrase in github_phrases):
            summary = f"{task.step}: {task.task}"
            description = task.description
            issue = create_github_issue(summary, description)
            if issue:
                task.github_issue = str(issue["number"])
                task.github_link = issue["url"]
            else:
                task.github_issue = None
                task.github_link = None
        else:
            task.github_issue = None
            task.github_link = None
    return tasks

def create_fallback_tasks(goal: str) -> List[TaskItem]:
    goal_lower = goal.lower()
    if any(keyword in goal_lower for keyword in ['mobile', 'app', 'ios', 'android']):
        return [
            TaskItem(
                step="Requirements Analysis",
                task="Define Functional and Non-Functional Requirements",
                description="Conduct stakeholder interviews, create user stories, define MVP features, and document technical requirements. Create a comprehensive requirements document including user personas, use cases, and acceptance criteria.",
                technologies=["Figma", "Jira", "Confluence", "User Story Mapping Tools"],
                deliverables=["Requirements Document", "User Stories", "MVP Feature List", "Technical Specifications"],
                estimated_time="1-2 weeks"
            ),
            TaskItem(
                step="Technical Architecture",
                task="Design System Architecture and Technology Stack",
                description="Design the overall system architecture, choose technology stack, plan database schema, and define API structure. Consider scalability, security, and maintainability requirements.",
                technologies=["React Native/Flutter", "Node.js/Python", "PostgreSQL/MongoDB", "AWS/Firebase", "REST/GraphQL"],
                deliverables=["Architecture Diagram", "Technology Stack Document", "Database Schema", "API Documentation"],
                estimated_time="1-2 weeks"
            ),
            TaskItem(
                step="UI/UX Design",
                task="Create User Interface and Experience Design",
                description="Design wireframes, create high-fidelity mockups, develop design system, and create interactive prototypes. Ensure responsive design and accessibility compliance.",
                technologies=["Figma", "Adobe XD", "Sketch", "InVision", "Design System Tools"],
                deliverables=["Wireframes", "High-fidelity Mockups", "Design System", "Interactive Prototype"],
                estimated_time="2-3 weeks"
            ),
            TaskItem(
                step="Backend Development",
                task="Develop Server-Side Logic and APIs",
                description="Set up development environment, implement authentication, create REST/GraphQL APIs, integrate with third-party services, and implement business logic with proper error handling and security measures.",
                technologies=["Node.js/Express", "Python/Django", "JWT", "Stripe/PayPal APIs", "AWS S3", "Redis"],
                deliverables=["API Endpoints", "Authentication System", "Database Models", "Third-party Integrations"],
                estimated_time="4-6 weeks"
            ),
            TaskItem(
                step="Frontend Development",
                task="Build Mobile Application Interface",
                description="Implement UI components, integrate with backend APIs, implement navigation, add state management, and ensure cross-platform compatibility with native features integration.",
                technologies=["React Native", "Flutter", "Redux/MobX", "Native Modules", "Push Notifications"],
                deliverables=["Mobile App Components", "API Integration", "Navigation System", "State Management"],
                estimated_time="4-6 weeks"
            ),
            TaskItem(
                step="Testing & Quality Assurance",
                task="Comprehensive Testing and Bug Fixing",
                description="Implement unit tests, integration tests, perform manual testing on multiple devices, conduct security testing, and optimize performance. Include accessibility testing and user acceptance testing.",
                technologies=["Jest", "Detox", "Appium", "Firebase Test Lab", "Security Testing Tools"],
                deliverables=["Test Suites", "Test Reports", "Performance Metrics", "Bug Fix Documentation"],
                estimated_time="2-3 weeks"
            ),
            TaskItem(
                step="Deployment & Launch",
                task="Deploy to App Stores and Production",
                description="Set up CI/CD pipeline, prepare app store listings, deploy backend to production servers, submit apps for review, and configure monitoring and analytics systems.",
                technologies=["GitHub Actions", "App Store Connect", "Google Play Console", "AWS/Heroku", "Analytics Tools"],
                deliverables=["Published Apps", "Production Environment", "CI/CD Pipeline", "Monitoring Dashboard"],
                estimated_time="1-2 weeks"
            )
        ]


    # One universal fallback plan (no project-type detection)
    return [
        TaskItem(
            step="Project Planning",
            task="Define Project Scope and Requirements",
            description="Analyze project requirements, define scope, create user stories, establish project timeline, and document requirements.",
            technologies=["Project Management Tools", "Documentation Platforms", "Requirement Analysis Tools"],
            deliverables=["Project Scope Document", "User Stories", "Timeline", "Requirements Specification"],
            estimated_time="1-2 weeks"
        ),
        TaskItem(
            step="System Design",
            task="Create Technical Architecture and Design",
            description="Design the system architecture, choose appropriate technology stack, create database schema, and plan API structure. Consider scalability, security, and performance requirements.",
            technologies=["System Design Tools", "Database Design Tools", "API Documentation Tools"],
            deliverables=["Architecture Diagram", "Database Schema", "API Design", "Technology Stack Selection"],
            estimated_time="1-2 weeks"
        ),
        TaskItem(
            step="Development Setup",
            task="Set Up Development Environment and Infrastructure",
            description="Set up development environment, configure version control, establish coding standards, and prepare deployment infrastructure. Include security configurations and monitoring setup.",
            technologies=["Git", "Docker", "CI/CD Tools", "Cloud Platforms", "Development IDEs"],
            deliverables=["Development Environment", "Git Repository", "Deployment Pipeline", "Coding Standards Document"],
            estimated_time="3-5 days"
        ),
        TaskItem(
            step="Core Development",
            task="Implement Core Functionality",
            description="Develop the main features and functionality of the application. Implement business logic, user authentication, data management, and core user workflows with proper error handling.",
            technologies=["Programming Languages", "Frameworks", "Databases", "Authentication Systems"],
            deliverables=["Core Application Features", "Authentication System", "Database Implementation", "API Endpoints"],
            estimated_time="4-8 weeks"
        ),
        TaskItem(
            step="Testing & QA",
            task="Test and Validate the System",
            description="Perform comprehensive testing including unit tests, integration tests, performance testing, and security testing. Conduct user acceptance testing and fix identified issues.",
            technologies=["Testing Frameworks", "Automated Testing Tools", "Performance Testing Tools", "Security Testing Tools"],
            deliverables=["Test Suites", "Test Reports", "Performance Metrics", "Security Assessment"],
            estimated_time="2-3 weeks"
        ),
        TaskItem(
            step="Deployment",
            task="Deploy to Production Environment",
            description="Deploy the application to production servers, configure monitoring and logging, set up backup systems, and ensure high availability. Include performance optimization and security hardening.",
            technologies=["Cloud Platforms", "Monitoring Tools", "Backup Solutions", "Security Tools"],
            deliverables=["Production Deployment", "Monitoring Dashboard", "Backup System", "Security Configuration"],
            estimated_time="1-2 weeks"
        )
    ]