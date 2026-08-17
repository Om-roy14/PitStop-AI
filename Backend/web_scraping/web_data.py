from langchain_community.document_loaders import WebBaseLoader
from openai import OpenAI
import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()
api_key =os.getenv("GROQ_API_KEY")
client = Groq(
    api_key=api_key
)
# client = Groq(api_key=api_key)
# url=input("here")
def get_structured_data(url):

    loader = WebBaseLoader(url)
    docs = loader.load()

    scraped_data = docs[0].page_content

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
Extract the job information from the provided webpage content.

Return ONLY valid JSON in this structure:

{
    "job_title": "",
    "company": "",
    "location": "",
    "salary": "",
    "experience": "",
    "job_type": "",
    "job_description": "",
    "responsibilities": [],
    "requirements": [],
    "skills": [],
    "perks": "",
    "application_deadline": ""
}

Do not invent information.
If a field is not available, use null.
"""
            },
            {
                "role": "user",
                "content": scraped_data
            }
        ]
    )

    structured_data = response.choices[0].message.content

    # print("\nDEBUG GEMINI RESPONSE:")
    # print(repr(structured_data))

    # structured_data = json.loads(structured_data)

    return structured_data