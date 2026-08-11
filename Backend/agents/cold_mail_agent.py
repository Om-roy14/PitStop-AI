from Backend.web_scraping.web_data import get_structured_data
import json

# url="https://internshala.com/job/detail/sales-team-lead-job-in-multiple-locations-at-sygnius-digital-private-limited1786106304"
url=input("ENTER YOUR MAIL HERE 👉")

job_data=get_structured_data(url)
job_data=json.loads(job_data)
print(job_data)