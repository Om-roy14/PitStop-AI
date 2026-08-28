import os
from dotenv import load_dotenv
from groq import Groq
from langchain_community.document_loaders import WebBaseLoader

# Load environment variables
load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# =========================================
# PROMPT DEFINITION
# =========================================
SYSTEM_PROMPT = """
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

# =========================================
# SCRAPING & EXTRACTION LOGIC
# =========================================
def get_structured_data(url: str) -> str:
    """Scrapes a URL and uses an LLM to extract structured job data."""
    
    # 1. Load the webpage content
    loader = WebBaseLoader(url)
    docs = loader.load()
    scraped_data = docs[0].page_content

    # 2. Extract structured data using Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": scraped_data}
        ]
    )

    # 3. Return the raw JSON string
    structured_data = response.choices[0].message.content.strip()
    return structured_data