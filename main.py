from google.genai import types
import streamlit as st
from google import genai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import re
import pandas as pd
from docx import Document
from pydantic import BaseModel

class ResumeAnalysis(BaseModel):
    summary: str
    key_skills: list[str]
    improvements: list[str]
    skills_score: int
    experience_score: int
    clarity_score: int
    overall_score: int


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Resume Analyzer", page_icon="🐬", layout="wide")
st.title("Resume Analyzer")
st.markdown("Upload resume and get a **summary, key skills, score, and improvement suggestions**")

uploaded_file = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])

if uploaded_file:
    text = ""
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif uploaded_file.type == "text/plain":
        uploaded_file.seek(0)
        text = uploaded_file.read().decode("utf-8")
    else:
        pdf = PdfReader(uploaded_file)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    text_clean = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Resume Preview")
        st.text_area("Resume Text", value=text_clean, height=400)

    with col2:
        st.subheader("AI Analysis")
        if st.button("Analyze Resume"):
            with st.spinner("Analyzing Resume..."):
                prompt = f"""
                You are a resume expert.
                Analyze the following resume provide:
                1. Summary
                2. List of key skills
                3. Suggestions for improvement
                4. Score out of 100 based on 
                    - skills match (30 pts)
                    - Experience and achievements (30 pts)
                    - Clarity & Formatting (30 pts)
                    - Overall impression (10 pts)
                Also provied the individual category score in JSON
                Resume:
                {text_clean}
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ResumeAnalysis,
                    ),
                )
                analysis: ResumeAnalysis = response.parsed

                print(analysis.summary)
                print(analysis.key_skills)
                total_score = analysis.skills_score + analysis.experience_score + analysis.clarity_score + analysis.overall_score
                st.subheader("Executive Summary")
                st.write(analysis.summary)

                st.subheader("Key Skills")
                st.write(", ".join(analysis.key_skills))

                st.subheader("Improvements & Recommendations")
                for imp in analysis.improvements:
                    st.markdown(f"- {imp}")

                st.subheader("Score Breakdown")
                score_data = {
                    "Skills Match": analysis.skills_score,
                    "Experience": analysis.experience_score,
                    "Clarity & Formatting": analysis.clarity_score,
                    "Overall Impression": analysis.overall_score,
                }

                df = pd.DataFrame(
                    {
                        "Category": list(score_data.keys()),
                        "Score": list(score_data.values()),
                    }
                )
                st.bar_chart(df.set_index("Category"))

                total_score = sum(score_data.values())
                st.metric(
                    label="Total Resume Score", value=f"{total_score} / 100"
                )
                st.progress(min(total_score / 100, 1.0))
               
