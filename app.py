import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import PyPDF2 as pdf

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model= genai.GenerativeModel("gemini-pro")
    response= model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page= reader.pages[page]
        text+= str(page.extract_text())

    return text

# Prompt template

input_prompt="""
Act like a very skilled or very experienced ATS(Application Tracking System) with a a deep understanding of tech field,
software engineering, data science, data analyst, machine learning engineer, and big data engineer.Your task is to evaluate
the resume based on the given job description.
You must consider the job market to be very competitive and you should provide the best assistance for improving the resumes.
Assign the percentage matching based on given Jd and the missing keywords necessary with high accuracy.

resume:{text}
description:{Jd}

I want the response in one single string having the structure{{"JD Match":"%","Missing Keywords:[]","Profile":""}}


"""


# Strealit App

st.title("Smart ATS")
st.text("Improve your resume ATS")
jd=st.text_area("Paste the Job description here")
uploaded_file= st.file_uploader("Upload your resume", type="pdf", help="Please upload the pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text= input_pdf_text(uploaded_file)
        response= get_gemini_response(input_prompt)
        st.subheader(response)