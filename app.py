import streamlit as st
import re
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
import pytesseract
import requests
import time
import os

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
# -----------------------------
# JOB DATA & RECOMMENDATIONS
# -----------------------------
JOB_DATA = {
    "Software Engineer": ["JavaScript", "React", "Node.js", "Python", "Git", "MySQL", "Data Structures & Algorithms", "Cloud Computing", "Docker", "REST APIs"],
    "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Statistics", "Data Visualization", "Pandas", "NumPy", "Scikit-learn", "TensorFlow/PyTorch", "Big Data"],
    "UX/UI Designer": ["Figma", "Sketch", "Adobe XD", "Wireframing", "Prototyping", "Visual Design", "HTML/CSS"],
}

RECOMMENDATION_DATA = {
    "Python": {
        "courses": [{"name": "Complete Python Pro Bootcamp", "link": "https://www.udemy.com/course/100-days-of-code/", "platform": "Udemy"}],
        "roadmap": ["Learn basic syntax", "Object-oriented programming", "NumPy/Pandas"],
        "projects": ["Web scraper", "CLI app", "Flask/Django app"]
    },
    "React": {
        "courses": [{"name": "React - The Complete Guide", "link": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "platform": "Udemy"}],
        "roadmap": ["Components, props, state", "Hooks", "Redux/Context API"],
        "projects": ["To-do app", "Portfolio website", "Weather app"]
    },
    "Git": {
        "courses": [{"name": "Git & GitHub Crash Course", "link": "https://www.udemy.com/course/git-and-github-crash-course/", "platform": "Udemy"}],
        "roadmap": ["Learn git commands", "Understand branching and merging", "Use GitHub for version control"],
        "projects": ["Collaborative coding project using Git", "Host code on GitHub"]
    },
    "Docker": {
        "courses": [{"name": "Docker Mastery", "link": "https://www.udemy.com/course/docker-mastery/", "platform": "Udemy"}],
        "roadmap": ["Learn containers", "Docker CLI basics", "Docker Compose"],
        "projects": ["Dockerize a Python/Node.js app", "Deploy multi-container app"]
    },
    "RESTful APIs": {
        "courses": [{"name": "REST API Design with Flask and Python", "link": "https://www.udemy.com/course/rest-api-flask-and-python/", "platform": "Udemy"}],
        "roadmap": ["Understand REST principles", "Learn Flask/Django API basics", "Test APIs with Postman"],
        "projects": ["Build a simple REST API", "Connect API to frontend app"]
    },
    "SQL": {
        "courses": [{"name": "The Complete SQL Bootcamp", "link": "https://www.udemy.com/course/the-complete-sql-bootcamp/", "platform": "Udemy"}],
        "roadmap": ["SELECT, FROM, WHERE", "JOINs & subqueries", "Window functions"],
        "projects": ["Analyze sales data", "Design a database schema", "Solve LeetCode SQL challenges"]
    },
    "Machine Learning": {
        "courses": [{"name": "Machine Learning by Andrew Ng", "link": "https://www.coursera.org/learn/machine-learning", "platform": "Coursera"}],
        "roadmap": ["Linear algebra basics", "Supervised/unsupervised learning", "Evaluate models"],
        "projects": ["Spam classifier", "Movie recommender", "Predict housing prices"]
    },
    "Data Visualization": {
        "courses": [{"name": "Data Visualization with Python", "link": "https://www.coursera.org/learn/python-for-data-visualization", "platform": "Coursera"}],
        "roadmap": ["Learn Matplotlib/Seaborn", "Understand data storytelling", "Build dashboards"],
        "projects": ["Visualize sales trends", "Interactive dashboard", "Plot public dataset"]
    },
    "Cloud Computing": {
        "courses": [{"name": "AWS Certified Cloud Practitioner", "link": "https://aws.amazon.com/certification/certified-cloud-practitioner/", "platform": "AWS"}],
        "roadmap": ["Learn IaaS/PaaS/SaaS", "Key services: compute/storage/databases", "Practice in AWS free tier"],
        "projects": ["Deploy static website on S3", "Host Node.js app on EC2", "Serverless function (Lambda)"]
    }
}


# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------
def escape_reg_exp(string):
    return re.escape(string)

def extract_text_from_pdf(file_bytes):
    """Extract text from normal PDF"""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except:
        return ""

def extract_text_from_scanned_pdf(file_bytes):
    """Extract text from scanned PDF using OCR"""
    try:
        pages = convert_from_bytes(file_bytes)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
        return text
    except:
        return ""

def extract_skills(text):
    words = re.split(r'[,\n; .]', text)
    all_skills = set(skill for skills in JOB_DATA.values() for skill in skills) | set(RECOMMENDATION_DATA.keys())
    extracted = [word.strip().title() for word in words if word.strip().title() in all_skills]
    return list(set(extracted))

def analyze_skills(resume_text, job_role):
    required_skills = JOB_DATA.get(job_role, [])
    user_skills = extract_skills(resume_text)
    matched_skills = [skill for skill in required_skills if skill in user_skills]
    missing_skills = [skill for skill in required_skills if skill not in user_skills]

    recommendations = {}
    for skill in missing_skills:
        rec = RECOMMENDATION_DATA.get(skill)
        if not rec:
            # Generic fallback for any missing skill
            rec = {
                "courses": [{"name": f"Learn {skill}", "link": "#", "platform": "Various"}],
                "roadmap": [f"Step 1: Understand basics of {skill}", 
                            f"Step 2: Practice {skill}", 
                            f"Step 3: Apply {skill} in a project"],
                "projects": [f"Build a small project using {skill}"]
            }
        recommendations[skill] = rec

    return {
        "job_role": job_role,
        "user_skills": user_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }


# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():
    st.set_page_config(page_title="AI Career Navigator Login", layout="centered")
    st.title("🔒 Login to AI Career Navigator")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    with st.form("login_form"):
        email = st.text_input("Email", key="email")
        password = st.text_input("Password", type="password", key="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if email.strip() == "" or password.strip() == "":
                st.warning("Please enter email and password.")
            else:
                st.session_state.logged_in = True
                st.success(f"Welcome, {email}!")
                st.rerun()



def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()

# -----------------------------
# ANALYZER PAGE
# -----------------------------
def analyzer_page():
    st.set_page_config(page_title="AI Career Navigator", layout="wide")
    st.title("🚀 AI Career Navigator")
    st.sidebar.button("Logout", on_click=logout)

    # --- Upload Resume ---
    uploaded_file = st.file_uploader(
        "Upload your resume (.pdf, .txt)",
        type=['pdf', 'txt']
    )

    resume_text = ""
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(file_bytes)
            if not resume_text.strip():
                resume_text = extract_text_from_scanned_pdf(file_bytes)
        else:
            resume_text = file_bytes.decode("utf-8")
        st.success(f"Loaded file: {uploaded_file.name}")

    # --- Job Role Selection ---
    job_role = st.selectbox(
        "Select a job role",
        options=["-- Select a role --"] + list(JOB_DATA.keys())
    )

    # --- Analyze Button ---
    if st.button("Analyze & Find Gaps"):
        if job_role == "-- Select a role --":
            st.warning("⚠️ Please select a job role.")
        elif not resume_text.strip():
            st.warning("⚠️ Could not read your resume. Try a text-based PDF or .txt file.")
        else:
            result = analyze_skills(resume_text, job_role)

            # Match score
            total_skills = len(result['matched_skills']) + len(result['missing_skills'])
            match_percentage = int((len(result['matched_skills']) / total_skills) * 100) if total_skills > 0 else 0
            st.subheader(f"Skill Match: {match_percentage}%")
            st.progress(match_percentage)

            # Matched / missing skills
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Matched Skills")
                for skill in result['matched_skills']:
                    st.success(skill)
            with col2:
                st.subheader("🔧 Skill Gaps")
                for skill in result['missing_skills']:
                    st.warning(skill)

            # Recommendations
            st.header("📚 Personalized Roadmap")
            if result['missing_skills']:
                for skill, rec in result['recommendations'].items():
                    with st.expander(f"Learn {skill}"):
                        if rec:
                            st.markdown("**Courses:**")
                            for course in rec['courses']:
                                st.markdown(f"- [{course['name']}]({course['link']}) on {course['platform']}")
                            st.markdown("**Projects:**")
                            for project in rec['projects']:
                                st.markdown(f"- {project}")
                            st.markdown("**Roadmap:**")
                            for step in rec['roadmap']:
                                st.markdown(f"- {step}")
            else:
                st.success("All required skills matched! Focus on projects and interviews.")

def chatbot_ui():
    """Career guidance AI chatbot in sidebar with resizable width."""
    
    # Slider to adjust chatbot width
    chat_width = st.sidebar.slider("🔧 Chatbot Width", min_value=250, max_value=600, value=350, step=10)
    
    # Apply custom CSS for dynamic width
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            width: {chat_width}px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.title("💬 Career Assistant")
        st.write("Ask me anything about skills, jobs, or interviews!")

        api_key = GEMINI_API_KEY  # use hardcoded key

        # Session state for messages
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi! I am your AI Career Assistant. How can I help you today?"}
            ]

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        if prompt := st.chat_input("Ask a question"):
            # Append user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Thinking..."):
                    response = call_gemini_api(prompt, api_key)
                    message_placeholder.markdown(response)

            # Store assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})



def call_gemini_api(user_input, api_key):
    """
    Calls the Gemini API to get career guidance answers.
    Returns the AI-generated response as a string.
    """
    if not api_key:
        return "API Key not provided."

    try:
        # System instructions to guide AI responses
        system_prompt = (
            "You are a world-class AI career coach. "
            "Provide concise, actionable advice about skill development, job search, interviews, and career growth. "
            "Use clear examples and recommend resources if possible."
        )

        # Gemini API endpoint
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

        # Payload to send to API
        payload = {
            "contents": [{"parts": [{"text": user_input}]}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
        }

        # Exponential backoff retry mechanism
        delay = 1
        response = None
        for _ in range(5):
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                break
            time.sleep(delay)
            delay *= 2

        if response and response.status_code == 200:
            result = response.json()
            # Extract AI response from JSON
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, could not generate a response.")
        else:
            error_text = response.text if response else "No response from server."
            return f"API call failed with status: {response.status_code if response else 'N/A'}. Error: {error_text}"

    except Exception as e:
        return f"An error occurred while connecting to the AI assistant: {e}"


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_page()
    else:
        chatbot_ui()
        analyzer_page()

if __name__ == "__main__":
    main()
