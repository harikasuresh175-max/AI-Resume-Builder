# AI Resume Builder and Career Guidance System

A beginner-friendly BCA project built with Python and Streamlit.

## Features
- Enter personal, education, skills, projects, certifications, and experience details.
- Generate a resume preview.
- Download the resume as TXT and PDF.
- Get career-role suggestions based on simple skill matching.
- See matching skills and skills to learn next.

> This is an academic prototype. Career suggestions are informational and do not guarantee employment.

## Run on Windows

1. Install Python 3.10 or newer from https://www.python.org/downloads/
2. Extract this ZIP file to a folder.
3. Open Command Prompt in that folder.
4. Install dependencies:

   ```bash
   py -m pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   py -m streamlit run app.py
   ```

6. Your browser should open the application. If not, copy the local URL shown in Command Prompt (usually `http://localhost:8501`) into your browser.

## Run in Anaconda Prompt

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Files
- `app.py` — main application source code
- `requirements.txt` — Python packages needed
- `README.md` — setup guide

## Suggested demo
Try these sample skills in Career Guidance:
`Python, SQL, HTML, CSS, communication, problem solving`

## Limitations and future improvements
- Role matching uses a small example list of skills, not a trained machine-learning model.
- No profiles are saved to a database.
- Future work could add more roles, resume templates, PDF styling, interview questions, and a database.
