# AI Resume Analyzer

An interactive web application built with **Streamlit** and the **Google GenAI SDK** that analyzes resumes (PDF, DOCX, or TXT), provides detailed qualitative feedback, and generates a quantitative score breakdown with visual charts.

---

## Features

* **Multi-Format Support:** Upload resumes in PDF, Word (`.docx`), or plain text (`.txt`) formats.
* **AI-Powered Evaluation:** Leverages the Gemini API (`gemini-2.5-flash`) to analyze summaries, extract key skills, and suggest improvements.
* **Quantitative Scoring:** Breaks down scores out of 100 based on skills match, experience/achievements, clarity & formatting, and overall impression.
* **Interactive Visualizations:** Displays score breakdowns using dynamic Streamlit bar charts and progress bars.

---

## Tech Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io/)
* **AI / LLM:** [Google GenAI SDK](https://github.com/google/genai-sdk) (`gemini-2.5-flash`)
* **File Parsers:** `PyPDF2`, `python-docx`
* **Data Handling:** `pandas`
* **Configuration:** `python-dotenv`

---

## Prerequisites

Make sure you have Python installed on your system (Python 3.8+ recommended). You will also need a Gemini API key from Google AI Studio.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/lukeklipping/ResumeAnalyzer.git](https://github.com/lukeklipping/ResumeAnalyzer.git)
   cd ResumeAnalyzer

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

3. **Install the dependencies:**
    ```bash
    pip install streamlit google-genai PyPDF2 python-dotenv pandas python-docx

4. **Setup environment variables**
    Create a .env file in the root directory of your project and add your Gemini API key:
    ```bash
    GEMINI_API_KEY=your_actual_api_key_here

### Running the Application Locally

To launch the Streamlit app locally, run:
```bash
streamlit run main_2.py
