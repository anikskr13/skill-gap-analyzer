import os
import json
from pydantic import BaseModel,Field
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

#========== Groq client api key connection =====================#
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY is missing")

client = Groq(api_key=my_api_key)
groq_model="openai/gpt-oss-120b"
#========== Groq client api key connection =====================#


#============= FETCH RESUME AND JD =========================#
## Documents Readers
import pdfplumber
from docx import Document

def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text

def read_docx(file_path):
    document = Document(file_path)
    text = ""
    # Read paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    # Read tables
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"

    return text

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def read_document(file_path):
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)

    elif file_path.suffix.lower() == ".docx":
        return read_docx(file_path)

    elif file_path.suffix.lower() == ".txt":
        return read_txt(file_path)

    else:
        print(f"Unsupported file format: {file_path.name}")


##=============================================================##

##=======================Resume data analysis ===========================================##
class CandidateProfile(BaseModel):
    name: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience_years: float | None = None
    education: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)

resume_schema = CandidateProfile.model_json_schema()
def parse_resume(resume_text):
    system_prompt = f"""
You are a professional resume information extraction assistant.

Extract a structured candidate profile from the resume text provided by the
user.

Rules:
1. Extract only facts explicitly stated in the resume.
2. Do not invent, guess, or infer missing information.
3. Keep skills, education, projects, and certifications as concise strings.
4. Convert experience to years only when the resume clearly states it.
5. Use null for missing optional values and [] for missing list values.
6. Return exactly one valid JSON object with no Markdown or explanation.
7. Follow this exact schema:

{resume_schema}
"""
    user_prompt = f"""
Extract the candidate profile from the resume below.

<resume_text>
{resume_text}
</resume_text>

Return one JSON object matching the schema from the system instructions.
"""

    message_system={
            "role" : "system",
            "content" : system_prompt
        }
    message_user={
        "role" : "user",
        "content" : user_prompt
        }
    messages=[message_system, message_user]
    response_format={"type":"json_object"}

    response=client.chat.completions.create(model=groq_model,messages=messages,response_format=response_format,temperature=0)
    answer=response.choices[0].message.content
    raw_json_output=answer #load the raw json ouput from LLM
    data=json.loads(raw_json_output)
    resume_data_object=CandidateProfile(**data)
    return resume_data_object
#=================================================================================#

##======================= Job Description data analysis ===============================##

class RoleRequirements(BaseModel):
    role_name: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    min_experience: float | None = None
    responsibilities: list[str] = Field(default_factory=list)


role_schema = RoleRequirements.model_json_schema()


def parse_job_description(jd_text):
    system_prompt = f"""
You are a professional job-description analysis assistant.

Extract structured role requirements from the job description provided by the
user.

Rules:
1. Extract only facts explicitly stated in the job description.
2. Put mandatory, essential, or required qualifications in required_skills.
3. Put bonus, desirable, or explicitly preferred qualifications in
   preferred_skills.
4. Never classify a preferred skill as required.
5. Extract min_experience only when a minimum is clearly stated.
6. Write responsibilities as concise factual strings.
7. Do not invent requirements, responsibilities, or experience values.
8. Use null for missing optional values and [] for missing list values.
9. Return exactly one valid JSON object with no Markdown or explanation.
10. Follow this exact schema:

{role_schema}
"""
    user_prompt = f"""
Extract the role requirements from the job description below.

<job_description>
{jd_text}
</job_description>

Return one JSON object matching the schema from the system instructions.
"""

    message_system = {
        "role": "system",
        "content": system_prompt
    }

    message_user = {
        "role": "user",
        "content": user_prompt
    }

    messages = [message_system, message_user]

    response_format = {"type": "json_object"}

    response = client.chat.completions.create(
        model=groq_model,
        messages=messages,
        response_format=response_format,
        temperature=0
    )

    answer = response.choices[0].message.content

    raw_json_output = answer
    data = json.loads(raw_json_output)

    role_data_object = RoleRequirements(**data)

    return role_data_object

##=====================================================================================##
