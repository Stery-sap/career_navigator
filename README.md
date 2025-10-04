# 🚀 AI Career Navigator
---
AI Career Navigator is a web application built with Python and Streamlit that helps users align their skills with their career goals. It analyzes resumes to identify skill gaps for specific job roles and provides a personalized roadmap with recommended courses, projects, and learning steps. The application also features an integrated AI-powered career assistant to answer user questions in real-time.

## ☁️ Live Demo
This application is deployed on Streamlit Cloud and can be accessed directly without any local installation.

➡️ [View the Live ](https://careernavigato-fg8hn3etzoxlaqwsoxutxa.streamlit.app/)
## ✨ Features

* **📄 Intelligent Resume Analysis:** Upload your resume in .pdf or .txt format. The app can process both text-based and scanned PDFs using OCR.

* **🎯 Skill Gap Identification:** Select a target job role (e.g., Software Engineer, Data Scientist) to see which skills you have and which you're missing.

* **🗺️ Personalized Roadmap:** Get a detailed, actionable plan to fill your skill gaps, including links to recommended online courses, relevant project ideas, and a step-by-step learning roadmap.

* **🤖 AI Career Assistant:** Chat with an AI assistant powered by the Gemini API. Ask questions about career paths, interview preparation, skill development, and more.

* **🔐 Simple Login:** A basic login page to simulate a user session.

* **Responsive UI:** The user interface is built with Streamlit for a clean, modern, and responsive experience.

## 🛠️ Running Locally
The following instructions are for developers who want to run the application on their local machine.

**Prerequisites**
Python: Make sure you have Python 3.8+ installed.

Tesseract OCR: This is required for reading scanned PDFs. Follow the installation guide for your operating system.

## Setup Steps
Clone the repository:

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration
The application requires a Gemini API key to power the AI chatbot.

For Local Development
Create a directory named .streamlit in the root of your project folder.

Inside this directory, create a new file named **secrets.toml**.

Add your Gemini API key to the secrets.toml file like this:
```bash
.streamlit/secrets.toml
```
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

▶️ Usage
Open your terminal in the project's root directory.

Run the following command:
```bash
python -m streamlit run app.py
```

The application will open automatically in your web browser.

## 💻 Technologies Used
Framework: Streamlit

PDF Processing: PyMuPDF (fitz), pdf2image

OCR: pytesseract

AI Model: Google Gemini API

Language: Python

