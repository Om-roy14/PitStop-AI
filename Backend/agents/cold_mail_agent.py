from Backend.web_scraping.web_data import get_structured_data
from openai import OpenAI
import groq
import os
from dotenv import load_dotenv
import json

client = OpenAI(
    api_key=os.getenv("COLD-EMAIL-API-KEY"),
    base_url="https://api.groq.com/openai/v1"
)

name=input("ENTER YOUR NAME 👉")
# url="https://internshala.com/job/detail/sales-team-lead-job-in-multiple-locations-at-sygnius-digital-private-limited1786106304"
url=input("ENTER YOUR MAIL HERE 👉")

job_data=get_structured_data(url)
# job_data=json.loads(job_data)
# print(job_data)

SYSTEM_PROMPT = f"""
You are an expert cold-email generation agent.

Your task is to write a highly personalized, professional, concise cold email based ONLY on the information available in the variables below.

SENDER NAME:
{name}

JOB DATA:
{job_data}

EMAIL REQUIREMENTS:

1. Write a professional cold email for applying to the job described in JOB DATA.
2. Personalize the email using the job title, company, required skills, responsibilities, experience, location, and other relevant information available in job_data.
3. Clearly express interest in the specific position.
4. Briefly connect the candidate's potential skills/experience to the requirements of the job.
5. Keep the email concise and easy to read. Ideally 120–180 words.
6. Do not repeat the entire job description.
7. Do not use generic statements that could apply to any company or job.
8. Do not invent:
   - skills
   - experience
   - qualifications
   - projects
   - achievements
   - education
   - company information
   - salary
   - contact information
   - recruiter name
9. If candidate-specific information is not available, do not pretend that it is. Focus on expressing interest and asking for an opportunity to discuss the role.
10. Use the company name and job title from job_data whenever available.
11. Use a natural and human tone. The email should not sound AI-generated or overly formal.
12. Avoid excessive flattery.
13. Do not use emojis.
14. Do not use hashtags.
15. Do not mention that you are an AI.
16. Do not mention job_data, variables, prompts, or these instructions.
17. Do not include placeholders such as [Company Name], [Your Name], etc.
18. End the email with the sender's actual name from the `name` variable.
19. Generate ONLY the email. Do not provide explanations before or after it.

EMAIL STRUCTURE:

Subject: A short, relevant subject related to the specific job.

Greeting:
Use a professional greeting. If a recruiter's/hiring manager's name is available in job_data, use it. Otherwise use "Dear Hiring Team,".

Opening:
Clearly state interest in the specific position and company.

Body:
Mention 1–2 relevant aspects of the job from job_data and naturally connect them to the candidate. Only use candidate information that is actually provided.

Closing:
Express interest in discussing the opportunity and politely request consideration.

Sign-off:
Best regards,
{name}
"""

def get_cold_email():
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": job_data}
        ]
    )
    result = response.choices[0].message.content.strip()
    print("\n\n")
    print( result)
    
    
get_cold_email()