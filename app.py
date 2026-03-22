import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 1. Load API Key (Works for local .env or Cloud Secrets)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def main():
    st.set_page_config(page_title="AI Talent Scout", page_icon="🤖")
    st.header("AI Resume Matcher 📄")
    st.markdown("---")

    # Check if API Key is missing
    if not api_key:
        st.error("API Key missing! Please set OPENAI_API_KEY in your Secrets or .env file.")
        return

    # 2. User Inputs
    st.subheader("Step 1: Paste Job Description")
    jd = st.text_area("What are the requirements for this role?", height=150)
    
    st.subheader("Step 2: Upload Candidate Resume")
    pdf = st.file_uploader("Upload PDF version only", type="pdf")

    # 3. Execution Logic
    if st.button("Analyze Match Score"):
        if pdf and jd:
            with st.spinner("AI is analyzing the candidate..."):
                try:
                    # Extract text from PDF
                    reader = PdfReader(pdf)
                    resume_text = ""
                    for page in reader.pages:
                        resume_text += page.extract_text()

                    # AI Instructions (Prompt)
                    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)
                    prompt = f"""
                    Role: Expert HR Recruiter
                    Task: Compare the Resume below against the Job Description (JD).
                    
                    JD: {jd}
                    Resume: {resume_text}
                    
                    Output Format:
                    - Match Score: [0-100]%
                    - Top 3 Reasons for Score:
                    - Missing Skills/Gaps:
                    """
                    
                    response = llm.invoke(prompt)
                    
                    # Display Results
                    st.success("Analysis Complete!")
                    st.markdown("### **Evaluation Results**")
                    st.write(response.content)
                
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please provide both the JD and the Resume PDF.")

if __name__ == "__main__":
    main()
