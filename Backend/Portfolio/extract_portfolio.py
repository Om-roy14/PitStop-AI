import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
from Backend.web_scraping.web_data import get_structured_data
from Backend.Databases.models import Portfolio, User
from sqlalchemy.orm import Session
load_dotenv()

client = OpenAI(
    api_key=os.getenv("COLD-EMAIL-API-KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# url = input("ENTER YOUR URL HERE 👉")

# job_data = get_structured_data(url)

project_data = pd.read_excel(
    "D:/PitStop/Backend/Portfolio/Om_Roy_Projects.xlsx"
)

def get_user_portfolio_context(db: Session) -> str:
  """Reads portfolio data from MySQL and formats it for the LLM."""
  projects = db.query(Portfolio).all()

  if not projects:
    return "No projects currently listed."

  # Format projects into structured text for the prompt
  context_lines = []
  for p in projects:
    context_lines.append(
        f"- Project: {p.Project_name} | Tech: {p.teck_stack} | Repo:"
        f" {p.github_repo}"
    )

  return "\n".join(context_lines)




SYSTEM_PROMPT = """
You are an expert project-selection agent for a job application system.

Your task is to analyze the provided JOB DATA and PROJECT DATA and select the projects
that are most relevant to the job.

JOB DATA:
{job_data}

PROJECT DATA:
{project_data}

OBJECTIVE:
Select only the projects that strongly match the job requirements.

MATCHING RULES:

1. Compare the job title, responsibilities, requirements, and required skills
   with each project's name and tech stack.

2. Give priority to projects whose:
   - Tech stack matches the required skills.
   - Project domain is relevant to the job.
   - Technologies directly mentioned in the job are used in the project.
   - Project functionality demonstrates skills required by the job.

3. Do NOT select projects simply because they are available.
   Select only genuinely relevant projects.

4. Prefer quality and relevance over quantity.

5. Select a maximum of 3 projects.

6. If only 1 or 2 projects are relevant, return only those projects.

7. If no project is sufficiently relevant, return an empty list.

8. Do not invent or modify project information.

9. Preserve the exact project name, tech stack, and Git repository link
   provided in PROJECT DATA.

10. Never create a Git repository link if one is not provided.

11. Do not include projects that have only a weak or superficial connection
    to the job.

OUTPUT FORMAT:

Return ONLY valid JSON.

{{
    "selected_projects": [
        {{
            "project_name": "",
            "tech_stack": "",
            "git_repo": ""
        }}
    ]
}}

If no relevant projects are found:

{{
    "selected_projects": []
}}
"""


def get_portfolio_data(job_data,db:Session):

    project_records = get_user_portfolio_context(db)

    prompt = SYSTEM_PROMPT.format(
        job_data=job_data,
        project_data=project_records
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )

    structured_data = response.choices[0].message.content

    return structured_data


# output = get_portfolio_data()

# print(output)