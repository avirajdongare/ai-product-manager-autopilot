import re
from typing import Union
from fpdf import FPDF

def extract_json_from_response(text: Union[str, dict]) -> str:
    """Extract JSON object from text, clean markdown."""
    if not isinstance(text, str):
        return text
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    return text

def generate_pdf_report(tasks, report_title="Project Plan Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, report_title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    for idx, task in enumerate(tasks, 1):
        pdf.cell(0, 10, f"{idx}. {task.step} - {task.task}", ln=True)
        pdf.set_font("Arial", style='I', size=10)
        pdf.cell(0, 8, f"Estimated Time: {task.estimated_time}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, f"Description: {task.description}")
        if task.technologies:
            pdf.multi_cell(0, 8, f"Technologies: {', '.join(task.technologies)}")
        if task.deliverables:
            pdf.multi_cell(0, 8, f"Deliverables: {', '.join(task.deliverables)}")
        if getattr(task, 'jira_link', None):
            pdf.cell(0, 8, f"Jira: {task.jira_link}", ln=True)
        pdf.ln(6)
    return pdf.output(dest='S').encode('latin1')

#uvicorn app.main:app --reload --port 5000