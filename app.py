import streamlit as st
import os
import sqlite3
import sys

# FIX: Force Streamlit to use a modern SQLite version
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

st.set_page_config(page_title="AI Recruiter Agent", page_icon="🤖")
st.title("🤖 AI Recruiter Agent (Week 2)")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    groq_key = st.text_input("Enter Groq API Key", type="password")
    st.info("Get your free key at: ://groq.com")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('recruiter.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS candidates')
    c.execute('CREATE TABLE candidates (id INTEGER, name TEXT, role TEXT, exp INTEGER, skills TEXT)')
    candidates = [
        (1, 'Alice Johnson', 'Python Developer', 5, 'Python, Django, SQL'),
        (2, 'Mark Chen', 'Frontend Engineer', 3, 'React, Tailwind, JS'),
        (3, 'Sarah Miller', 'AI Engineer', 2, 'LangChain, Groq, Python')
    ]
    c.executemany('INSERT INTO candidates VALUES (?,?,?,?,?)', candidates)
    conn.commit()
    conn.close()
    return SQLDatabase.from_uri("sqlite:///recruiter.db")

db = init_db()

# --- AGENT LOGIC ---
if groq_key:
    try:
        llm = ChatGroq(groq_api_key=groq_key, model="llama3-8b-8192", temperature=0)
        agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True)

        query = st.text_input("Search Candidates:", placeholder="e.g., Find a dev with 5+ years experience")

        if query:
            with st.spinner("Agent is thinking..."):
                response = agent_executor.invoke({"input": query})
                st.success("Analysis Complete:")
                st.write(response["output"])
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("👈 Please enter your Groq API Key in the sidebar!")

 
                
