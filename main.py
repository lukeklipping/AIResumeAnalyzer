import streamlit as st
from google import genai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import re
import pandas as pd

load_dotenv()
client = genai(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Resume Analyzer", page_icon="🐬", layout="wide")
st.title("Resume Analyzer")
st.markdown("Upload resume and get a **summary, key skills, score, and improvement suggestions **")

uploaded_file = st.file_uploader("Upload resume", type=["pdf"])

if uploaded_file:
    pdf = PdfReader(uploaded_file)
    text = ""
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
                    - Overall impression (20 pts)
                Also provied the individual category score in JSON
                Resume:
                {text_clean}
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                result = response.choices[0].message.content

                parts = result.split("Score JSON: ")
                analysis_text = parts[0]
                st.write(analysis_text)

                if len(parts) > 1:
                    try:
                        import json
                        score_data = json.loads(parts[1].strip())
                        st.subheader("Score breakdown")
                        df = pd.DataFrame({
                            "Category": list(score_data.keys()),
                            "Score": list(score_data.values())
                        })
                        st.bar_chart(df.set_index("Cateogory"))
                        total_score = sum(score_data.values())
                        st.progress(min(total_score / 100), 1.0)
                    except: 
                        st.warning("could not parse json")
                
