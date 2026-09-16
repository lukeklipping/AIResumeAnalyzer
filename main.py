import streamlit as st
from openai import OpenAI
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import re
import pandas as pd

load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

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

   
                
