# ResuMind — AI-Powered Resume Analyser

An AI-powered resume analysis application that helps job seekers evaluate their resumes against job descriptions, identify skill gaps, and receive actionable recommendations for improvement.

ResuMind combines resume text extraction with Google's Gemini AI to generate structured feedback and help candidates improve their resumes for specific job opportunities.

## Overview

Applying for internships and jobs often requires tailoring a resume to different job descriptions. ResuMind simplifies this process by analysing resume content, evaluating its relevance to a target role, and highlighting areas that could be improved.

Users can upload a resume, optionally provide a job description, and receive AI-generated analysis through a web interface.

## Features

- **Resume Upload:** Upload resumes in PDF and DOCX formats.
- **Text Extraction:** Extract readable text from uploaded documents.
- **AI-Powered Analysis:** Use Google Gemini to analyse resume content.
- **ATS-Oriented Feedback:** Receive feedback on resume quality and relevance to a target role.
- **Job Description Matching:** Compare resume content against a supplied job description.
- **Skill Gap Identification:** Identify potentially missing or underrepresented skills.
- **Actionable Suggestions:** Get recommendations for improving resume content and presentation.
- **Web Interface:** Access the application through a browser.
- **REST API:** Use FastAPI endpoints for application functionality and health checks.

*Note: AI-generated scores and recommendations are estimates, not guarantees of compatibility with any particular applicant tracking system (ATS) or employer.*

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | Backend web framework and REST API |
| Google Gemini API | AI-powered resume analysis |
| pdfplumber | PDF text extraction |
| python-docx | DOCX text extraction |
| Jinja2 | HTML template rendering |
| HTML, CSS, JavaScript | Frontend interface |
| Uvicorn | ASGI server |
| python-dotenv | Environment variable management |
| Git and GitHub | Version control and project hosting |

## How It Works

1. The user opens the ResuMind web application.
2. The user uploads a resume in PDF or DOCX format.
3. The backend extracts the resume text.
4. The user optionally provides a job description.
5. The application prepares the extracted text and relevant instructions for the Gemini model.
6. Gemini generates structured resume feedback.
7. The application returns the analysis to the user through its interface.

## Project Structure

```text
resumind-resume-analyser/
├── app.py
├── analyzer.py
├── parser.py
├── prompt.py
├── requirements.txt
├── .gitignore
├── templates/
│   └── index.html
├── static/
├── uploads/
└── README.md
```

The `static/` directory contains frontend assets, while `templates/` contains the HTML templates. The `uploads/` directory is used for uploaded resume files.

## Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.12 or another compatible Python version
- Git
- A Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/ananya722-pixel/resumind-resume-analyser.git
cd resumind-resume-analyser
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use an appropriate execution policy for your current session or activate the environment through your preferred terminal.

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key.

**Security warning:** Never commit your `.env` file or publish your API key on GitHub. Keep `.env` excluded through `.gitignore`.

### 5. Run the Application

Start the FastAPI development server:

```bash
uvicorn app:app --reload
```

Open the application in your browser:

**Web application:** http://127.0.0.1:8000

**API documentation:** http://127.0.0.1:8000/docs

**Health check:** http://127.0.0.1:8000/health

The `--reload` option automatically restarts the development server when application code changes. It is intended for development, not production deployment.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the web interface |
| GET | `/health` | Returns the application health status |
| POST | `/analyze` | Accepts a resume and optional job description for analysis |

The `/analyze` endpoint accepts a resume file and an optional `job_description` form field. Refer to the automatically generated API documentation at `/docs` for request details and available response schemas.

## Supported Resume Formats

| Format | Extension |
|---|---|
| Portable Document Format | `.pdf` |
| Microsoft Word Document | `.docx` |

Text extraction quality depends on the document structure. Scanned PDFs may require OCR support if their text is not selectable.

## Security and Privacy

- Keep API keys in environment variables.
- Exclude `.env` and virtual environment directories from version control.
- Avoid committing personal resumes or other sensitive uploaded documents.
- Validate uploaded files and handle malformed documents safely.
- Do not expose API credentials in frontend JavaScript or public repositories.

Uploaded files should be handled according to the application's storage and cleanup logic. Do not assume that uploaded resumes are automatically deleted unless cleanup is implemented.

## Current Scope and Limitations

- Analysis quality depends on the resume text, supplied job description, and AI model response.
- AI-generated scores are indicative assessments rather than official ATS scores.
- Complex layouts, tables, graphics, and scanned documents can affect text extraction.
- Results may vary between analyses.
- The application requires a valid Gemini API key and network access to the configured model.
- Production deployment may require additional authentication, rate limiting, logging, file-size limits, and data-retention controls.

## Future Improvements

Potential enhancements include:

- More detailed keyword and skill matching.
- Improved ATS-oriented formatting checks.
- Exportable analysis reports.
- Resume improvement suggestions tailored to specific roles.
- OCR support for scanned resumes.
- Stronger file validation and automatic upload cleanup.
- Automated tests and deployment configuration.
- User authentication and analysis history.

## Learning Outcomes

This project provides practical experience with:

- Building a Python web application using FastAPI.
- Integrating a generative AI API.
- Extracting text from PDF and DOCX documents.
- Designing prompts for structured AI responses.
- Managing dependencies and environment variables.
- Connecting backend processing with a browser-based interface.
- Using Git and GitHub for source control.

## Author

**Ananya Gupta**

B.Tech Computer Science and Engineering — Artificial Intelligence

GitHub: [@ananya722-pixel](https://github.com/ananya722-pixel)

## License

No license has been specified yet. Unless a license is added to this repository, the project should not be assumed to be available for unrestricted reuse or redistribution.


