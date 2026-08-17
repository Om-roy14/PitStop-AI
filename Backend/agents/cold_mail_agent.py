from Backend.web_scraping.web_data import get_structured_data
from Backend.Portfolio.extract_portfolio import get_portfolio_data
from openai import OpenAI
import groq
import os
from dotenv import load_dotenv
import json
from sqlalchemy.orm import Session
from Backend.Databases.database import SessionLocal  # Import your SessionLocal


client = OpenAI(
    api_key=os.getenv("COLD-EMAIL-API-KEY"),
    base_url="https://api.groq.com/openai/v1"
)

name=input("ENTER YOUR NAME 👉")
url=input("ENTER YOUR MAIL HERE 👉")
db = SessionLocal()

job_data=get_structured_data(url)
portfolio_data=get_portfolio_data(job_data,db=db)


SYSTEM_PROMPT = f"""
You are an expert cold-email generation agent.

Your task is to write a highly personalized, professional, concise cold email
for a job application using ONLY the information provided in:

1. SENDER NAME
2. JOB DATA
3. PORTFOLIO DATA

========================
SENDER NAME
========================

{name}


========================
JOB DATA
========================

{job_data}


========================
PORTFOLIO DATA
========================

{portfolio_data}


========================
OBJECTIVE
========================

Write a personalized cold email that connects the sender's relevant portfolio
projects and technologies with the requirements of the specific job.

The email should demonstrate why the sender's existing projects are relevant
to the position without exaggerating or inventing experience.


========================
EMAIL REQUIREMENTS
========================

1. Clearly express interest in the specific job position and company.

2. Use the job title and company name from JOB DATA whenever available.

3. Analyze the requirements, responsibilities, and skills mentioned in JOB DATA.

4. Use PORTFOLIO DATA to identify the most relevant projects for the job.

5. Mention only the portfolio projects that are genuinely relevant to the job.

6. For each mentioned project, use the exact:
   - Project name
   - Tech stack
   - Git repository link
   provided in PORTFOLIO DATA.

7. Do not mention every project in the portfolio. Focus only on the strongest
   matches for the specific job.

8. Naturally connect the selected projects to the skills or responsibilities
   mentioned in JOB DATA.

9. Do not invent:
   - skills
   - work experience
   - qualifications
   - education
   - achievements
   - project features
   - project results
   - technologies
   - GitHub links
   - company information
   - recruiter information
   - salary
   - contact information

10. Do not claim professional/work experience simply because a technology
    appears in a portfolio project.

11. Do not exaggerate the importance or complexity of any project.

12. If PORTFOLIO DATA does not contain a relevant project, do not force a
    project into the email.

13. If a Git repository link is available and useful, include it naturally.
    Do not create or modify a GitHub URL.

14. Keep the email concise and easy to read.
    Target approximately 120–180 words.

15. Do not repeat the entire job description.

16. Avoid generic statements that could apply to any company or position.

17. Use a natural, confident and human tone.

18. Avoid excessive flattery.

19. Do not use emojis.

20. Do not use hashtags.

21. Do not mention that you are an AI.

22. Do not mention JOB DATA, PORTFOLIO DATA, variables, prompts,
    instructions, or the generation process.

23. Do not use placeholders such as:
    [Company Name]
    [Your Name]
    [Recruiter Name]
    [GitHub Link]

24. End the email with the sender's actual name from the SENDER NAME variable.

25. Generate ONLY the email. Do not provide explanations before or after it.


========================
EMAIL STRUCTURE
========================

Subject:
Create a short and relevant subject based on the specific job.

Greeting:
If a recruiter or hiring manager name is available in JOB DATA, use it.
Otherwise use:

Dear Hiring Team,


Opening:
Clearly state interest in the specific position and company.


Personalization:
Briefly explain why the sender is relevant to the position.

Use 1–2 of the strongest matching portfolio projects.

For example, naturally connect:
JOB REQUIREMENT → RELEVANT PROJECT → TECHNOLOGY USED

Do not simply list projects.


Portfolio:
Mention the most relevant project(s) from PORTFOLIO DATA.

Include the Git repository link only when it adds value.


Closing:
Express interest in discussing the opportunity and politely request
consideration.


Sign-off:

Best regards,
{name}
"""

def get_cold_email():
    response=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": job_data}
        ]
    )
    result = response.choices[0].message.content.strip()
    print("\n\n")
    print( result)
    # return result
    
    
get_cold_email()
#  python -m Backend.agents.cold_mail_agent   to run
