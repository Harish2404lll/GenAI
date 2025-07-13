import streamlit as st
import requests
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AI Resume & Cover Letter Generator",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #222 !important;
    }
    .generated-content {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        white-space: pre-wrap;
        font-family: 'Georgia', serif;
        line-height: 1.6;
        color: #222 !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .error-message {
        background-color: #ffebee;
        color: #c62828;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f44336;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Resume & Cover Letter Generator</h1>
    <p>Create professional resumes and cover letters powered by Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# API Key input (more secure approach)
st.sidebar.header("🔐 API Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password", help="Get your API key from Google AI Studio")

if not api_key:
    st.warning("⚠️ Please enter your Gemini API key in the sidebar to continue.")
    st.info("🔗 Get your free API key from: https://makersuite.google.com/app/apikey")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📋 Personal Information")
    name = st.text_input("👤 Full Name")
    job_role = st.text_input("🧑‍💻 Target Job Role")
    skills = st.text_area("📄 Skills & Technologies")
    education = st.text_area("🏫 Education")
    experience = st.text_area("🏢 Previous Experience")
    job_description = st.text_area("💼 Job Description (Optional)")
    resume_style = st.selectbox("Resume Style", ["Professional", "Modern", "Creative", "Academic"])
    experience_level = st.selectbox("Experience Level", ["Entry Level/Fresher", "Mid-Level", "Senior Level"])

with col2:
    st.header("🎯 Quick Tips")
    st.markdown("""
    <div class="info-box">
    <strong>💡 Tips:</strong>
    <ul>
    <li>Use relevant keywords</li>
    <li>Highlight certifications</li>
    <li>Be concise and results-driven</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Function to call Gemini API (Fixed version)
def call_gemini_api(prompt, max_tokens=1000):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": max_tokens,
            "stopSequences": []
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Check if the response contains the expected structure
        if 'candidates' in result and len(result['candidates']) > 0:
            if 'content' in result['candidates'][0]:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Error: No content generated. Please try again."
        else:
            return f"Error: Unexpected response format. {result}"
            
    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}"
    except KeyError as e:
        return f"Response parsing error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Prompt builders
def build_resume_prompt():
    context = f"""
Create a {resume_style.lower()} resume for {name}, applying for a {job_role} role.
Experience Level: {experience_level}

Personal Information:
- Name: {name}
- Target Role: {job_role}

Skills & Technologies:
{skills}

Education:
{education}

Previous Experience:
{experience}
"""
    
    if job_description:
        context += f"\nJob Description to tailor the resume to:\n{job_description}"
    
    context += """

Please create a well-formatted resume with the following sections:
- Contact Information
- Professional Summary
- Skills
- Experience
- Education
- Additional relevant sections if applicable

Use bullet points for experience and achievements. Make it professional and tailored to the target role.
"""
    
    return context

def build_cover_letter_prompt():
    prompt = f"""
Write a professional cover letter for {name}, applying for a {job_role} position.
Experience Level: {experience_level}

Background Information:
Skills: {skills}
Education: {education}
Experience: {experience}
"""
    
    if job_description:
        prompt += f"\nJob Description:\n{job_description}"
    
    prompt += """

Please write a compelling cover letter that:
- Opens with enthusiasm for the specific role
- Highlights relevant skills and experience
- Shows understanding of the company/role requirements
- Demonstrates value proposition
- Closes with a call to action
- Keeps it concise (300-400 words)
- Uses professional tone

Format it as a proper business letter.
"""
    
    return prompt

# Buttons and output
if name and job_role and skills:
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("📄 Generate Resume", use_container_width=True):
            st.subheader("📄 Generated Resume")
            with st.spinner("Creating resume..."):
                resume = call_gemini_api(build_resume_prompt(), max_tokens=2000)
                if resume.startswith("Error:") or resume.startswith("Request Error:"):
                    st.markdown(f'<div class="error-message">{resume}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="generated-content">{resume}</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Download Resume", resume, f"{name.replace(' ', '_')}_Resume.txt")

    with col_btn2:
        if st.button("📝 Generate Cover Letter", use_container_width=True):
            st.subheader("📝 Generated Cover Letter")
            with st.spinner("Creating cover letter..."):
                letter = call_gemini_api(build_cover_letter_prompt(), max_tokens=1500)
                if letter.startswith("Error:") or letter.startswith("Request Error:"):
                    st.markdown(f'<div class="error-message">{letter}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="generated-content">{letter}</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Download Cover Letter", letter, f"{name.replace(' ', '_')}_CoverLetter.txt")

else:
    st.info("👆 Please fill in at least the Name, Job Role, and Skills fields to generate documents.")

# Footer
st.markdown("""
---
<center style="color: gray">
Built with ❤️ using Streamlit & Gemini API
</center>
""", unsafe_allow_html=True)
